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


class UserListCreate(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = AuthUserSerializer


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid Email"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check the password
        if user.check_password(password):        
            serializer = AuthUserSerializer(user)
            return Response(
                {"user": serializer.data}, status=status.HTTP_200_OK
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
