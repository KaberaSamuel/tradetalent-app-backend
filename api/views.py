from .serializers import UserSerializer
from api.models import User

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserListCreate(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
            serializer = UserSerializer(user)
            return Response(
                {"user": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
     permission_classes = [IsAuthenticated]

    #  Invalidating the token after logout
     def post(self, request):
          try:  
               print("invalidating token")
               refresh_token = request.data["refresh"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)

class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data})
