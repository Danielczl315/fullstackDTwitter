from .models import Post, Reply
from rest_framework import serializers 
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager

"""
Create and Delete 
"""
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'media']

"""
Read 
"""
class GetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

"""
Create and Delete 
"""
class ReplySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Reply
        fields = ['text', 'media']


"""
Read 
"""
class GetReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', "user", "replying_to", 'text', 'media', 'created_at']