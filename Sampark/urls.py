"""
URL configuration for Sampark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Sampark/', include('auth_system.urls')),
    path('Sampark/', include('mail.urls')),
 
    path('', lambda request: HttpResponse("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Welcome to Sampark</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    background-color: #f9fafb;
                    color: #333;
                }
                .container {
                    padding: 100px 20px;
                }
                h1 {
                    font-size: 48px;
                    color: #1e293b;
                }
                h2 {
                    font-size: 22px;
                    color: #334155;
                    margin-bottom: 30px;
                }
                a {
                    color: #2563eb;
                    text-decoration: none;
                    font-weight: 500;
                }
                a:hover {
                    text-decoration: underline;
                }
                .footer {
                    margin-top: 50px;
                    font-size: 14px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📧 Sampark</h1>
                <h2>A smart email & OTP API platform to integrate mailing in your projects.</h2>
                
                <p>To get started:</p>
                <p>
                    <a href='/Sampark/signup/'>Signup</a> |
                    <a href='/Sampark/login/'>Login</a>
                </p>

                <div style="margin-top: 30px;"></div>

                <p>Check out the 
                    <a href='https://github.com/yourusername/sampark' target="_blank">GitHub Repository</a>.
                </p>
                
                <div style="margin-top: 30px;"></div>

                <p>Contact: 
                    <a href='mailto:contactdarshan07@gmail.com'>contactdarshan07@gmail.com</a>
                </p>

                <div class="footer">
                    Developed by Darshan Sharma
                </div>
            </div>
        </body>
        </html>
    """)),
]
