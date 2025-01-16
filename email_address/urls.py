from django.urls import path
from .views import *

urlpatterns = [
    path("email_address_list/", Email_Address_List_View.as_view())
]
