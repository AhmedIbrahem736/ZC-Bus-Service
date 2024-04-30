from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from apps.users.serializers import RegistrationSerializer


class RegistrationAPI(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)
