from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
urlpatterns = [
    path('api-token-auth/', obtain_auth_token,
         name='api_token_auth'),
    path('account/register/', views.AccountRegisterView.as_view(),
         name='register'),
    path('account/login/', views.AccountLoginView.as_view(),
         name='login'),
]
