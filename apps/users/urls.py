from django.urls import path
from apps.users.views import RegistrationAPI


urlpatterns = [
    path("registration/", RegistrationAPI.as_view()),
]
