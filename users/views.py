import os, logging
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.html import strip_tags

from django.template.loader import render_to_string
from google.auth.transport import requests
from google.oauth2 import id_token

from rest_framework import status, filters
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import (
    AuthUserSerializer,
    HomeUserSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
)

from users.models import User, PasswordReset

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        google_token = request.data.get("token")

        try:
            # Verify Google token
            idinfo = id_token.verify_oauth2_token(
                google_token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            # Extract user info
            email = idinfo["email"]
            name = idinfo.get("name", "")

            # Get or create user
            user, created = User.objects.get_or_create(
                email=email, defaults={"name": name}
            )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Return user data and tokens
            serializer = HomeUserSerializer(user)
            return Response(
                {
                    "user": serializer.data,
                    "tokens": {"access": str(access_token), "refresh": str(refresh)},
                },
                status=status.HTTP_200_OK,
            )

        except ValueError:
            return Response(
                {"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid Email"}, status=status.HTTP_400_BAD_REQUEST
            )

        if user.check_password(password):
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # get user data for homepage
            serializer = HomeUserSerializer(user)
            return Response(
                {
                    "user": serializer.data,
                    "tokens": {"access": str(access_token), "refresh": str(refresh)},
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    #  Invalidating the token after logout
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class HomeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        serializer = HomeUserSerializer(request.user)
        return Response({"user": serializer.data})

    def post(self, request):
        serializer = HomeUserSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = HomeUserSerializer
    lookup_field = "slug"


class SearchView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = HomeUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "about", "services_offered", "services_needed"]

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordReset(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = f"{os.environ['FRONTEND_URL']}/public/reset-password/{token}"

            # Sending reset link via email
            html_content = render_to_string(
                "request_password_reset.html", {"link": reset_url}
            )
            plain_message = strip_tags(html_content)
            send_mail(
                subject="Reset Your Service Exchange App Password",
                message=plain_message,
                from_email=f"Service Exchange App <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=False,
            )

            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "User with credentials not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_obj = PasswordReset.objects.filter(token=request.data["token"]).first()

        if not reset_obj:
            return Response({"error": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(request.data["password"])
            user.save()
            reset_obj.delete()
            return Response({"success": "Password updated"})
        else:
            return Response({"error": "No user found"}, status=404)
