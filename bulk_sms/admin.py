from django.contrib import admin


# Register your models here.
from .models import *
admin.site.register(SmsConfiguration)
admin.site.register(SmsCompose)
admin.site.register(SandBox)
admin.site.register(SmsRecipients)