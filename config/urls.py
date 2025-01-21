from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('mail.urls')),
    path('api/v1/', include('account.urls')),
    path('api/v1/email_address/', include('email_address.urls')),
    path('api/v1/bulk_sms/', include('bulk_sms.urls'))
]
