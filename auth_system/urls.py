from django.urls import path
from .views import Signup , GenerateAPIKey,  Logout , Login , RefreshTokenView

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('generate-api-key/', GenerateAPIKey.as_view(), name='generate-api-key'),
    
]