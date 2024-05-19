from django.contrib.auth import password_validation
from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User, PasswordStatus, WalletTransaction


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'wallet_balance', 'password_status', 'groups']


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, validators=[password_validation.validate_password])
    confirm_password = serializers.CharField(max_length=128)

    @staticmethod
    def validate_email(value: str):
        email = value.lower()
        index = email.find("@")
        domain = email[index:]
        if domain != "@zewailcity.edu.eg":
            raise serializers.ValidationError("email must be a Zewail City email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        return email

    @staticmethod
    def validate_first_name(value: str):
        return value.capitalize()

    @staticmethod
    def validate_last_name(value: str):
        return value.capitalize()

    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError("password and confirm password must be the same")

        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        instance = User.objects.create_user(**validated_data)

        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError("User is not verified.")

        data['user'] = ReadUserSerializer(instance=self.user).data

        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=4, max_length=4)

    def validate_otp(self, value):
        user = self.context['user']

        if user.password_status != PasswordStatus.OTP_REQUIRED:
            raise serializers.ValidationError("No OTP was requested")

        if user.otp_sent_at < timezone.now() - timedelta(minutes=5):
            raise serializers.ValidationError("OTP has expired")

        if user.otp != value:
            raise serializers.ValidationError("OTP is incorrect")

        return value

    def update(self, instance, validated_data):
        instance.otp = None
        instance.otp_sent_at = None
        instance.password_status = PasswordStatus.CHANGEABLE
        instance.is_verified = True
        instance.save()

        return instance


class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, validators=[password_validation.validate_password])
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        user = self.context['user']
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        # check that password is changeable
        if user.password_status != PasswordStatus.CHANGEABLE:
            raise serializers.ValidationError("No OTP is verified")

        if password != confirm_password:
            raise serializers.ValidationError("password and confirm password must be the same")

        return attrs

    def update(self, instance, validated_data):
        password = validated_data['password']
        instance.set_password(password)
        instance.password_status = PasswordStatus.UNCHANGEABLE
        instance.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128, validators=[password_validation.validate_password])
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        user = self.context['user']
        old_password = attrs['old_password']
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if not user.check_password(old_password):
            raise serializers.ValidationError("old password is incorrect")

        if new_password != confirm_password:
            raise serializers.ValidationError("new password and confirm password must be the same")

        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()
        return instance


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        exclude = ['is_safe_deleted']
