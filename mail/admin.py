from django.contrib import admin
from .models import OTPConfiguration, EmailRecord , APIKey , EmailCredential


admin.site.register(OTPConfiguration)
admin.site.register(EmailRecord)
admin.site.register(APIKey)
admin.site.register(EmailCredential)
