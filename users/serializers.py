from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    class Meta:
        model = User 
        fields = [ "first_name", "last_name", "email", "password"] 
        extra_kwargs = {
            'password': {'write_only': True} 
        }

    
    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'location', 'about', 
                 'services_offered', 'services_needed', 'profile_image']
    
    def update(self, instance, validated_data): 
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.location = validated_data.get('location', instance.location)
        instance.about = validated_data.get('about', instance.about)
        instance.services_offered = validated_data.get('services_offered', instance.services_offered)
        instance.services_needed = validated_data.get('services_needed', instance.services_needed)
        
        instance.save()
        return instance
    
