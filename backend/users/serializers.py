from .models import User, Profile
from rest_framework import serializers 
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'wallet_address', 'date_joined', 'new_user'] 
    
class ProfileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Profile
        fields = ['bio', 'name', 'profile_url', 'banner_url'] 
