from rest_framework import serializers
from users.serializers import HomeUserSerializer
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    user = HomeUserSerializer(read_only=True)

    class Meta:
        model = Listing
        exclude = ('id',)
    
    