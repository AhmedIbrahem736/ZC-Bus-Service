from rest_framework import serializers
from .models import Semester
from datetime import datetime
from django.utils import timezone

class SemesterSerializer(serializers.ModelSerializer):
    is_valid_to_subscribe = serializers.SerializerMethodField()
    class Meta:
        model = Semester
        fields = ['id', 'year', 'semester_name', 'subscribe_valid_from', 'subscribe_valid_to', 'is_valid_to_subscribe']

    def get_is_valid_to_subscribe(self, obj):
        current_date = timezone.now().date()
        print("obj.subscribe_valid_from", obj.subscribe_valid_from)
        print("obj.subscribe_valid_to", obj.subscribe_valid_to)
        return obj.subscribe_valid_from <= current_date <= obj.subscribe_valid_to


    def validate_year(self, value):
        current_year = datetime.now().year
        if value not in [current_year, current_year + 1]:
            raise serializers.ValidationError("Year must be either the current year or the next year.")
        return value

    def validate_semester_name(self, value):
        if value not in dict(Semester.SEMESTER_CHOICES).keys():
            raise serializers.ValidationError("Invalid semester name.")
        return value

    def validate_subscribe_valid_from(self, value):
        try:
            date_value = datetime.strptime(str(value), "%Y-%m-%d").date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format.")
        current_year = timezone.now().year
        next_year = current_year + 1
        if not (current_year <= date_value.year <= next_year):
            raise serializers.ValidationError("Date must be between this year and next year.")
        return value

    def validate_subscribe_valid_to(self, value):
        try:
            date_value = datetime.strptime(str(value), "%Y-%m-%d").date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format.")
        current_year = timezone.now().year
        next_year = current_year + 1
        if not (current_year <= date_value.year <= next_year):
            raise serializers.ValidationError("Date must be between this year and next year.")
        return value