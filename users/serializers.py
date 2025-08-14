from rest_framework import serializers
from users.models import User

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {'write_only': True} 
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
        )
        return user

class HomeUserSerializer(serializers.ModelSerializer):
    name_initials = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User 
        fields = ['email', 'name', 'location', 'about', 
                 'services_offered', 'services_needed', 'profile_image', 'name_initials', 'first_name']

    def get_name_initials(self, obj):
        name_parts = obj.name.split(" ")
        name_initials = ''
        if len(name_parts) == 1:
            name_initials = name_parts[0][0]
        else:
            first_name, *middle_name, last_name = name_parts
            name_initials = f"{first_name[0]}{last_name[0]}"
        return name_initials.upper()
    
    def get_first_name(self, obj):
        return obj.name.split(" ")[0]

    def to_representation(self, instance):
        """Custom method to format profile_image to return complete image url """
        data = super().to_representation(instance)
        if instance.profile_image:
            data['profile_image'] = str(instance.profile_image.url)
        else:
            data['profile_image'] = None
        return data
    
    def update(self, instance, validated_data):
        """update only changed fields with valid data"""
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance