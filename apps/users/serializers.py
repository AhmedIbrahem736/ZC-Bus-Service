from django.contrib.auth import password_validation
from rest_framework import serializers
from apps.users.models import User


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
