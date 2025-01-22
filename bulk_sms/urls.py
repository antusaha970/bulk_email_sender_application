from django import urls
from django.urls import path
from .views import *

urlpatterns = [
    path('sms_config/',SmsConfigurationView.as_view(),name="sms_configaration"),
    path('sms_compose/',SmsComposeView.as_view(),name="sms_compose"),
    path('sms_compose/<int:compose_id>/',SpecificComposeView.as_view(),name="view_specific_compose"),
    path('view_sandbox/',SandboxView.as_view(),name="view_sandbox"),
    path('view_recipients/',RecipentsView.as_view(),name="view_recipients"),
    path("recipient_numbers_list/", Recipient_Number_List_View.as_view(),name="excel_recipient_number")

    # path()
]