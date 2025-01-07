from django.urls import path
from .views import MailView
urlpatterns = [
    path('send_mail/', MailView.as_view())
]
