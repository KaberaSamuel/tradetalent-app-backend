from rest_framework import serializers
from users.models import User

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email', 'password', 'first_name', 'last_name']
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


class HomeUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    name_initials = serializers.SerializerMethodField()
    
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'location', 'about', 
                 'services_offered', 'services_needed', 'profile_image', 'name_initials']
    
    # get full url for the profile image
    def get_profile_image(self, obj):
        if obj.profile_image:
            return str(obj.profile_image.url)
        return None

    def get_name_initials(self, obj):
        if obj.first_name and obj.last_name:
            return (obj.first_name[0] + obj.last_name[0]).upper()
        return ""

    
    def update(self, instance, validated_data): 
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.location = validated_data.get('location', instance.location)
        instance.about = validated_data.get('about', instance.about)
        instance.services_offered = validated_data.get('services_offered', instance.services_offered)
        instance.services_needed = validated_data.get('services_needed', instance.services_needed)
        
        # Handle profile image upload
        if 'profile_image' in validated_data:
            instance.profile_image = validated_data.get('profile_image')
            
        instance.save()
        return instance
    


    
