from rest_framework import serializers
from .models import EmailCredential, APIKey, EmailRecord, OTPConfiguration


class EmailCredentialSerializer(serializers.ModelSerializer):
    email_host_password = serializers.CharField(write_only=True)

    class Meta:
        model = EmailCredential
        fields = ['email_host_user', 'email_host_password']

    def create(self, validated_data):
        # Add default values
        validated_data['smtp_host'] = 'smtp.gmail.com'
        validated_data['smtp_port'] = 587
        validated_data['use_tls'] = True

        return EmailCredential.objects.create(**validated_data)


    def create(self, validated_data):
        password = validated_data.pop('email_host_password')
        user = self.context['request'].user
        email_credential = EmailCredential.objects.create(
            user=user,
            **validated_data
        )
        email_credential.set_password(password)
        email_credential.save()
        return email_credential


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['api_key', 'api_duration', 'created_at']


class EmailRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRecord
        fields = ['recipient_email', 'subject', 'email_body', 'mail_type', 'status', 'sent_at']


class OTPConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPConfiguration
        fields = ['otp_digits']


class SendEmailSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    email_body = serializers.CharField()


class SendEmailResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    otp_code = serializers.CharField(required=False, allow_blank=True)
