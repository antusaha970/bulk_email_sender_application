from django.urls import path
from .views import MailView, EmailComposeView, ViewsSpecificMail, SMTPConfigurationView
urlpatterns = [
    path('send_mail/', MailView.as_view()),
    path('view_mails/', EmailComposeView.as_view()),
    path('view_mails/<int:id>/', ViewsSpecificMail.as_view()),
    path('configurations/', SMTPConfigurationView.as_view()),
    path('configurations/', SMTPConfigurationView.as_view()),
]
