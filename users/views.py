from .serializers import AuthUserSerializer, HomeUserSerializer
from users.models import User

from django.contrib.auth import authenticate
from rest_framework.permissions import  AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


class Register(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
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
            return Response({
                "user": serializer.data,
                "tokens": {"access": str(access_token),
                "refresh": str(refresh)},
            }, status=status.HTTP_200_OK)
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

class Home(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        serializer = HomeUserSerializer(request.user)
        return Response({"user": serializer.data})
    
    def post(self, request):
        serializer = HomeUserSerializer(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
