from rest_framework import serializers
from apps.bus.models import BusRoute, BusStop, BusSubscription, BusOffering
import re
import datetime


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = ['id','name', 'address', 'map_location', 'departure_time', 'arrival_time', 'bus_route']

    def validate_map_location(self, value):
        if not value:
            raise serializers.ValidationError("Map location cannot be empty.")
        pattern = r'^-?([1-8]?[1-9]|[1-9]0)\.\d{1,6}, ?-?((1[0-7]|[1-9])?\d(\.\d{1,6})?|180(\.0{1,6})?)$'
        if not re.match(pattern, value):
            # like '29.7604, -95.3698'
            raise serializers.ValidationError("Invalid map location format. Must be in the format 'latitude, longitude'.")
        return value


class BusRouteSerializer(serializers.ModelSerializer):
    bus_stops = BusStopSerializer(many=True, read_only=True)

    class Meta:
        model = BusRoute
        fields = ['id', 'destination', 'code', 'driver', 'capacity', 'plate_number', 'bus_stops']
        
    def validate_route_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Route name must be at least 5 characters long.")
        return value
    
    def validate_code(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Code must be at least 3 characters long.")
        return value
    
    def validate_driver(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Driver must be an active user.")
        return value
    

    def validate_capacity(self, value):
        if not (10 <= value <= 200):
            raise serializers.ValidationError("Capacity must bet between 10 and 200")
        return value
    
    def validate_plate_number(self, value):
        if not re.match(r'^[\u0621-\u064A0-9\s]+$', value):
            raise serializers.ValidationError("Plate number must contain only Arabic characters, numbers, or spaces.")
        return value

    def create(self, validated_data):
        date_now = datetime.date.today()
        try:
            validated_data['bus_offering'] = BusOffering.objects.get(is_safe_deleted=False,
                                                                     start_date__lte=date_now, end_date__gte=date_now)
        except:
            raise serializers.ValidationError('There is no bus offering at the moment')

        return super().create(validated_data)


class BusSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusSubscription
        exclude = ['is_safe_deleted']
        read_only_fields = ['start_date', 'end_date', 'amount_paid']

    def validate(self, attrs):
        user = attrs['user']
        date_now = datetime.date.today()
        if BusSubscription.objects.filter(user=user, is_safe_deleted=False,
                                          bus_route__bus_offering__start_date__lte=date_now,
                                          bus_route__bus_offering__end_date__gte=date_now).exists():
            raise serializers.ValidationError('You cannot subscribe to multiple subscriptions per same offering')

        return attrs

    def create(self, validated_data):
        validated_data['start_date'] = validated_data['bus_route'].bus_offering.start_date
        validated_data['end_date'] = validated_data['bus_route'].bus_offering.end_date
        validated_data['amount_paid'] = validated_data['bus_route'].bus_offering.subscription_amount

        return super().create(validated_data)
