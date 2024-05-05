from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from apps.users.models import User, PasswordStatus
from apps.users.serializers import (RegistrationSerializer, EmailSerializer, UpdatePasswordSerializer,
                                    ChangePasswordSerializer, VerifyOtpSerializer)


class RegistrationAPI(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class SendOtpAPI(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = EmailSerializer

    def get_object(self):
        email = self.request.data['email']
        return get_object_or_404(User, email=email)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.otp = '1234'
        user.otp_sent_at = timezone.now()
        user.password_status = PasswordStatus.OTP_REQUIRED
        user.save()

        # send OTP to user via email

        return Response(status=status.HTTP_200_OK)


class VerifyOtpAPI(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = VerifyOtpSerializer

    def get_object(self):
        email = self.request.data['email']
        return get_object_or_404(User, email=email)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data,
                                         partial=True, context={'user': instance})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class UpdatePasswordAPI(UpdateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        email = self.request.data['email']
        return get_object_or_404(User, email=email)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data,
                                         partial=True, context={'user': instance})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class ChangePasswordAPI(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data,
                                         partial=True, context={'user': instance})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
