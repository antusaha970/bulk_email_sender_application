from django.contrib import admin
from .models import *

admin.site.register(Email_Compose)
admin.site.register(SMTPConfiguration)
admin.site.register(Recipient)
admin.site.register(Outbox)
admin.site.register(Attachment)
