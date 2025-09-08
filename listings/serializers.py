import pendulum
from rest_framework import serializers
from users.serializers import HomeUserSerializer
from .models import Listing
from pprint import pprint

class ListingSerializer(serializers.ModelSerializer):
    user = HomeUserSerializer(read_only=True)
    date = serializers.SerializerMethodField()
    delta_time = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = ['id', 'user', 'title', 'type', 'slug', 'work_mode', 'location', 'description', 'skills', 'date', 'delta_time']

    def get_date(self, obj): 
        date = pendulum.instance(obj.created_at)
        formated_date = date.format('MMMM D, YYYY')
        return formated_date
    
    def get_delta_time(self, obj):
        """Custom method to get a date string for when a listing was posted"""
        target_date = pendulum.instance(obj.created_at)
        delta_time = target_date.diff_for_humans()
        return delta_time

  