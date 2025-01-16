from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('mail.urls')),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include('email_address.urls')),
    path('api/v2/', include('bulk_sms.urls'))
]
