from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views import UsernameValidationView, EmailValidationView

urlpatterns = [

    path('register', views.register, name='register'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()) , name='validate-email')
]

