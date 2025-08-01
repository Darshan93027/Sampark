from django.db import models
import uuid
from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet
import base64


class EmailCredential(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_credentials"
    )
    email_host_user = models.EmailField()
    email_host_password_encrypted = models.BinaryField()  # save this in encrypted format
    smtp_host = models.CharField(max_length=100, default='smtp.gmail.com')
    smtp_port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, password):
        """Encrypt and store password"""
        key = settings.SECRET_KEY.encode()[:32]
        key = base64.urlsafe_b64encode(key)
        f = Fernet(key)
        self.email_host_password_encrypted = f.encrypt(password.encode())

    def get_password(self):
        """Decrypt and return password"""
        key = settings.SECRET_KEY.encode()[:32]
        key = base64.urlsafe_b64encode(key)
        f = Fernet(key)
        return f.decrypt(self.email_host_password_encrypted).decode()

    def __str__(self):
        return f"Email credentials for {self.user.username}"


def generate_short_uuid():
    return str(uuid.uuid4()).replace("-", "")[:8]


class APIKey(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="api_key"
    )
    api_key = models.CharField(max_length=8, unique=True)
    api_duration = models.PositiveIntegerField(default=5)  # Expires in 5 days
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            new_key = generate_short_uuid()
            while APIKey.objects.filter(api_key=new_key).exists():
                new_key = generate_short_uuid()
            self.api_key = new_key
        super().save(*args, **kwargs)

    def __str__(self):
        return f"API Key for {self.user.username}: {self.api_key}"


class EmailRecord(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    
    MAIL_TYPE_CHOICES = (
        ('normal', 'Normal Mail'),
        ('otp', 'OTP Mail'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_records"
    )
    email_credential = models.ForeignKey(
        EmailCredential,
        on_delete=models.CASCADE,
        related_name="email_records"
    )
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    email_body = models.TextField()
    mail_type = models.CharField(max_length=10, choices=MAIL_TYPE_CHOICES, default='normal')
    otp_code = models.CharField(max_length=8, blank=True, null=True)  # For OTP emails
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    sent_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Email to {self.recipient_email} - {self.status}"


class OTPConfiguration(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otp_config"
    )
    otp_digits = models.IntegerField(choices=[(4, '4 digits'), (6, '6 digits'), (8, '8 digits')], default=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OTP Config for {self.user.username} - {self.otp_digits} digits"

