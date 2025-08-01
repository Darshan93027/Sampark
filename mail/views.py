from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import EmailCredential, APIKey, EmailRecord, OTPConfiguration
from .serializers import (
    EmailCredentialSerializer, 
    APIKeySerializer, 
    EmailRecordSerializer, 
    OTPConfigurationSerializer,
    SendEmailSerializer
)
from django.utils import timezone
from datetime import timedelta
from .utils import send_email_with_user_credentials


class EmailCredentialView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Add/Update SMTP credentials for the authenticated user"""
        serializer = EmailCredentialSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Delete existing credentials if any
            EmailCredential.objects.filter(user=request.user).delete()
            
            # Create new credentials
            email_credential = serializer.save()
            
            return Response({
                "message": "SMTP credentials saved successfully.",
                "email": email_credential.email_host_user
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Get user's SMTP credentials"""
        try:
            credential = EmailCredential.objects.get(user=request.user)
            return Response({
                "email_host_user": credential.email_host_user,
                "smtp_host": credential.smtp_host,
                "smtp_port": credential.smtp_port,
                "use_tls": credential.use_tls
            }, status=status.HTTP_200_OK)
        except EmailCredential.DoesNotExist:
            return Response({
                "message": "No SMTP credentials found. Please add your credentials first."
            }, status=status.HTTP_404_NOT_FOUND)


class SendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, api_key):
        """
        Send email using API key passed in URL and query param 'code'.
        URL example: /send-email/<api_key>/?code=1
        """
        code = request.GET.get("code")  # fetch ?code=xxx

        try:
            api_key_obj = APIKey.objects.get(api_key=api_key)

            # Check if API key expired
            if hasattr(api_key_obj, "api_duration"):
                expiry_date = api_key_obj.created_at + timedelta(days=api_key_obj.api_duration)
                if timezone.now() > expiry_date:
                    return Response({"error": "API key has expired."},
                                    status=status.HTTP_401_UNAUTHORIZED)

            # Get user's email credentials
            try:
                email_credential = EmailCredential.objects.get(user=api_key_obj.user)
            except EmailCredential.DoesNotExist:
                return Response({
                    "error": "SMTP credentials not found. Please add your email credentials first."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate request data
            serializer = SendEmailSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data

                result = send_email_with_user_credentials(
                    email_credential=email_credential,
                    recipient_email=data['recipient_email'],
                    subject=data['subject'],
                    body=data['email_body'],
                    code=code,
                    otp_digits=data.get('otp_digits', 6),
                    user=api_key_obj.user
                )

                return Response(
                    result,
                    status=status.HTTP_200_OK if result['success']
                    else status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except APIKey.DoesNotExist:
            return Response({"error": "Invalid API key."}, status=status.HTTP_401_UNAUTHORIZED)

class EmailRecordsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user's email records"""
        records = EmailRecord.objects.filter(user=request.user).order_by('-sent_at')
        serializer = EmailRecordSerializer(records, many=True)
        
        return Response({
            "records": serializer.data,
            "total_count": records.count()
        }, status=status.HTTP_200_OK)


class OTPConfigurationView(APIView):
    permission_classes = [IsAuthenticated]
    
    # def post(self, request):
    #     """Add/Update OTP configuration for the authenticated user"""
    #     serializer = OTPConfigurationSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         # Delete existing configuration if any
    #         OTPConfiguration.objects.filter(user=request.user).delete()
            
    #         # Create new configuration
    #         config = serializer.save()
            
    #         return Response({
    #             "message": "OTP configuration saved successfully.",
    #             "config": OTPConfigurationSerializer(config).data,
    #             "api": "https://api.sampark.com/<api_key>/mail/send?code=2",
    #         }, status=status.HTTP_201_CREATED)
        

    def post(self, request):
        """Add/Update OTP configuration for the authenticated user"""
        serializer = OTPConfigurationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Delete existing configuration if any
            OTPConfiguration.objects.filter(user=request.user).delete()
            
            # Create new configuration with user assigned
            config = serializer.save(user=request.user)
            
            return Response({
                "message": "OTP configuration saved successfully.",
                "config": OTPConfigurationSerializer(config).data,
                "api": "http://localhost:8000/Sampark/<api_key>/mail/send?=2"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        """Get user's OTP configuration"""
        try:
            config = OTPConfiguration.objects.get(user=request.user)
            serializer = OTPConfigurationSerializer(config)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OTPConfiguration.DoesNotExist:
            return Response({
                "message": "OTP configuration not found."
            }, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        """Update user's OTP configuration"""
        try:
            config = OTPConfiguration.objects.get(user=request.user)
            serializer = OTPConfigurationSerializer(config, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "OTP configuration updated successfully.",
                    "config": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OTPConfiguration.DoesNotExist:
            return Response({
                "message": "OTP configuration not found."
            }, status=status.HTTP_404_NOT_FOUND)

