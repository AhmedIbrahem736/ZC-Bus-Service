from rest_framework import serializers
from .models import Subscription
from datetime import datetime
from django.utils import timezone
from apps.users.models import User

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'semester', 'bus_route']

    def validate_user(self, value):
        # TODO must be later to be dynamicall set
        min_wallet_balance = 4500  
        if value.wallet_balance < min_wallet_balance:
            raise serializers.ValidationError("User's wallet balance must be above a certain value.")
        
        return value

    def validate_semester(self, value):
        current_date = timezone.now().date()
        if not (value.subscribe_valid_from <= current_date <= value.subscribe_valid_to):
            raise serializers.ValidationError("Semester is not currently open for subscription.")
        return value
    
    def validate_bus_route(self, value):
        current_subscriptions = Subscription.objects.filter(bus_route=value, semester=self.initial_data['semester'])
        total_subscribed_users = current_subscriptions.count()
        bus_route_capacity = value.capacity
        if total_subscribed_users >= bus_route_capacity:
            raise serializers.ValidationError("This bus route has reached its capacity.")
        return value


class ReadUserSerializer(serializers.ModelSerializer):
    subscribed_route = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'subscribed_route']

    def get_subscribed_route(self, user):
        try:
            # Get the latest subscription of the user
            subscription = user.subscription_set.latest('created_at')
            bus_route = subscription.bus_route
            return {'id': bus_route.id, 'destination': bus_route.destination}
        except Subscription.DoesNotExist:
            return None