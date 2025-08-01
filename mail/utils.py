import random
import string
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from .models import OTPConfiguration, EmailRecord


def generate_otp(digits=6):
    """Generate OTP with specified number of digits"""
    return ''.join(random.choices(string.digits, k=digits))


def send_email_with_user_credentials(email_credential, recipient_email, subject, body, code, otp_digits=6, user=None):
    """
    If code == "1": send normal mail
    If code == "2": generate OTP mail + msg
    """

    #Default mail type
    mail_type = "normal"
    otp_value = None

    # If user has OTP configuration, override digits
    try:
        otp_config = OTPConfiguration.objects.get(user=user)
        otp_digits = otp_config.otp_digits
    except OTPConfiguration.DoesNotExist:
        pass  # keep default otp_digits

    # Handle OTP mail (code == "2")
    if str(code) == "2":
        mail_type = "otp"
        otp_value = generate_otp(otp_digits)
        #user body and otp both append to the same body means user custom msg and our otp service both works together 
        #first user msg and in last OTP msg will be appended
        body = f"{body}\n\nYour OTP is: {otp_value}"

    try:
        # Use SMTP config from email credential
        connection = get_connection(
            host=email_credential.smtp_host,
            port=email_credential.smtp_port,
            username=email_credential.email_host_user,
            password=email_credential.get_password(),
            use_tls=email_credential.use_tls,
        )

        # Send email
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=email_credential.email_host_user,
            to=[recipient_email],
            connection=connection,
        )
        email.send()

        # Log record
        EmailRecord.objects.create(
            user=user,
            email_credential=email_credential,
            recipient_email=recipient_email,
            subject=subject,
            email_body=body,
            mail_type=mail_type,
            otp_code=otp_value if mail_type == "otp" else None,
            status="sent"
        )

        response = {"success": True, "message": "Mail sent successfully"}
        if mail_type == "otp":
            response["otp"] = otp_value
        return response

    except Exception as e:
        # Log failed record
        EmailRecord.objects.create(
            user=user,
            email_credential=email_credential,
            recipient_email=recipient_email,
            subject=subject,
            email_body=body,
            mail_type=mail_type,
            otp_code=otp_value if mail_type == "otp" else None,
            status="failed",
            error_message=str(e)
        )
        return {"success": False, "error": str(e)}
