from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.base.models import CustomBaseModel
from phonenumber_field.modelfields import PhoneNumberField
from apps.users.managers import CustomUserManger


class PasswordStatus(models.TextChoices):
    CHANGEABLE = 'Changeable'
    OTP_REQUIRED = 'OTP required'
    UNCHANGEABLE = 'Unchangeable'


class User(AbstractUser, CustomBaseModel):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile = PhoneNumberField(unique=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    otp = models.CharField(max_length=4, null=True)
    otp_sent_at = models.DateTimeField(null=True)
    password_status = models.CharField(max_length=50, choices=PasswordStatus.choices,
                                       default=PasswordStatus.UNCHANGEABLE)

    objects = CustomUserManger()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
