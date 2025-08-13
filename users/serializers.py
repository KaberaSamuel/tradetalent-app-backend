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
    profile_image = serializers.SerializerMethodField()
    name_initials = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User 
        fields = ['email', 'name', 'location', 'about', 
                 'services_offered', 'services_needed', 'profile_image', 'name_initials', 'first_name']
    

    def get_profile_image(self, obj):
        if obj.profile_image:
            return str(obj.profile_image.url)
        return None

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

    
    def update(self, instance, validated_data):  
        instance.name = validated_data.get('name', instance.name)
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
    


    
