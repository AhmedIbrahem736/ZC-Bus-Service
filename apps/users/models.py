from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError
from apps.base.models import CustomBaseModel
from phonenumber_field.modelfields import PhoneNumberField
from apps.users.managers import CustomUserManger


class PasswordStatus(models.TextChoices):
    CHANGEABLE = 'Changeable'
    OTP_REQUIRED = 'OTP required'
    UNCHANGEABLE = 'Unchangeable'


class WalletTransactionMethod(models.TextChoices):
    ONLINE = 'Online'
    OFFLINE = 'Offline'


class WalletTransactionType(models.TextChoices):
    DEPOSIT = 'Deposit'
    WITHDRAWAL = 'Withdrawal'
    SUBSCRIPTION = 'Subscription'
    RESERVATION = 'Reservation'


class User(AbstractUser, CustomBaseModel):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile = PhoneNumberField(unique=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    otp = models.CharField(max_length=4, null=True)
    otp_sent_at = models.DateTimeField(null=True)
    password_status = models.CharField(max_length=50, choices=PasswordStatus.choices,
                                       default=PasswordStatus.UNCHANGEABLE)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManger()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def add_to_wallet(self, amount, transaction_type, transaction_method):
        self.wallet_balance += amount
        self.save()

        WalletTransaction.objects.create(user=self, amount=amount,
                                         transaction_type=transaction_type,
                                         transaction_method=transaction_method)

    def subtract_from_wallet(self, amount, transaction_type, transaction_method):
        if amount > self.wallet_balance:
            raise ValidationError('Your balance is below the amount.')

        self.wallet_balance -= amount
        self.save()

        WalletTransaction.objects.create(user=self, amount=amount,
                                         transaction_type=transaction_type,
                                         transaction_method=transaction_method)


class WalletTransaction(CustomBaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='wallet_transactions')
    transaction_method = models.CharField(max_length=30, choices=WalletTransactionMethod.choices, null=False)
    transaction_type = models.CharField(max_length=30, choices=WalletTransactionType.choices, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=3, null=False)
