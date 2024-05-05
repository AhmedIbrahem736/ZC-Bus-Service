from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.views import RegistrationAPI, SendOtpAPI, UpdatePasswordAPI, ChangePasswordAPI, VerifyOtpAPI


urlpatterns = [
    path("registration/", RegistrationAPI.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("forget-password/", SendOtpAPI.as_view()),
    path("verify-otp/", VerifyOtpAPI.as_view()),
    path("resend-otp/", SendOtpAPI.as_view()),
    path("update-password/", UpdatePasswordAPI.as_view()),
    path("<int:pk>/change-password/", ChangePasswordAPI.as_view()),
]
