from django.urls import path
from .views import *
from auth_system.views import GenerateAPIKey

urlpatterns = [
    path('credentials/', EmailCredentialView.as_view(), name='email-credentials'),
    path('send-email/<str:api_key>/', SendEmailView.as_view(), name='send-email'),
    path('records/', EmailRecordsView.as_view(), name='email-records'),
    path('otp-config/', OTPConfigurationView.as_view(), name='otp-config'),
    path('refresh-api-key/', GenerateAPIKey.as_view(), name='refresh-api-key'),
] 