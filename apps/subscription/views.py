from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Subscription
from .serializers import SubscriptionSerializer, ReadUserSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from apps.users.models import User

class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # I can subscire only if semester is open
        # i can't subscribe twice a semester
        if not request.user.has_perm('subscription.add_subscription'):
            raise PermissionDenied("You do not have permission to subscribe to a bus route.")
        request.data['user'] = request.user.id
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        # Subtract min_wallet_balance from user's wallet_balance
        # TODO the value of subscription must be dynamic
        # TODO add to transcations models when creatd
        min_wallet_balance = 4500
        request.user.wallet_balance -= min_wallet_balance
        request.user.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class SubscribedUsersListView(generics.ListAPIView):
    serializer_class = ReadUserSerializer

    def get_queryset(self):
        semester_id = self.kwargs.get('semester_id')
        # Get all subscriptions for the given semester
        subscriptions = Subscription.objects.filter(semester_id=semester_id)
        # Extract the user IDs from subscriptions
        user_ids = subscriptions.values_list('user_id', flat=True)
        # Get the users subscribed for the semester
        return User.objects.filter(id__in=user_ids)
