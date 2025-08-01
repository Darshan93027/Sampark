from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from mail.models import APIKey, OTPConfiguration
import uuid

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken as JWTRefreshToken
class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # directly create user

            return Response({
                "message": "User registered successfully.",
                "user_id": user.id,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Check user exists
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

            # Authenticate using username (Django uses username field internally)
            user = authenticate(username=user_obj.username, password=password)

            if user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                return Response({
                    "message": "Login successful.",
                    "user_id": user.id,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials."},
                                status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateAPIKey(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        duration = request.data.get('duration', 5)  # Default 5 days
        
    
        APIKey.objects.filter(user=user).delete()
        
        # Generate new API key
        api_key = APIKey.objects.create(
            user=user,
            api_duration=duration
        )
        
        return Response({
            "message": "API key generated successfully.",
            "api_key": api_key.api_key,
            "duration": api_key.api_duration,
            "created_at": api_key.created_at,
            "api" : "http://localhost:8000/Sampark/<api_key>/mail/send?=2"
        }, status=status.HTTP_201_CREATED)


class Logout(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Error during logout."}, status=status.HTTP_400_BAD_REQUEST)
  
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = JWTRefreshToken(refresh_token)
                access_token = token.access_token
                return Response({
                    "access_token": str(access_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No refresh token provided."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Error while refreshing token."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)