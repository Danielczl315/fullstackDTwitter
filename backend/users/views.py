from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .serializers import UserSerializer
# backend views
from .forms import CustomUserCreationForm
from .models import User, Profile

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# api 

from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from rest_framework.serializers import ValidationError 

from . import serializers  
from . import utils
from . import authentication


# api testing 
from django.contrib.auth import authenticate

class SignInView(views.APIView):
    # only logged in user can log out 
    permission_classes = (permissions.AllowAny, )

    def post(self, request): 
        username, password = request.data['username'], request.data['password']
        user = authenticate(username=username, password=password)
        login(request, user) 
        data = {'success': 'Sucessfully logged in'}
        return Response(data=data, status=status.HTTP_200_OK)


class NonceView(views.APIView): 
    permission_classes = (permissions.AllowAny, )

    def get(self, request): 
        data = {} 
        address = request.GET['wallet_address']
        try:
            user = User.objects.get(wallet_address=address)
        except User.DoesNotExist:
            print('hi')
            user = User.objects.create_user(username=utils.generate_random_name(), wallet_address=address)
            # extended profile entry
            Profile.objects.create(user=user)
        # django can't set username empty, so we need to store an extra field 
        data['new_user'] = user.new_user
        data['nonce'] = user.nonce
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request): 
        address = request.data['address']
        signature = request.data['signature'] 
        nonce = request.data['nonce']
        message = request.data['message']
        user = User.objects.get(wallet_address=address)

        if user.nonce != nonce: 
            return Response({'message': 'Invalid Nonce'}, status=status.HTTP_403_FORBIDDEN)
        if utils.verify_signature(address, signature, message): 
            user.nonce = utils.generate_nonce() 
            user.save() 
            login(request, user) 
            return Response({'user': user.username}, status=status.HTTP_200_OK)
        return Response({'message': 'signature not verified'}, status=status.HTTP_403_FORBIDDEN) 

class OnboardingView(views.APIView): 
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request): 
        # init user 
        user = request.user
        user_data = {}
        # this is only set once 
        user_data['username'] = request.data['username']
        # set new_user to false 
        user_data['new_user'] = False 
        user_serializer = serializers.UserSerializer(user, data=user_data, partial=True) 
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        # init profile 
        profile = request.user.profile
        profile_data = {}        
        if 'profile_img' in request.data:
            profile_data['profile_url'] = request.data['profile_img'] 
            # rename 
            profile_data['profile_url'].name = str(request.user.id) + '.' + profile_data['profile_url'].name.split('.')[-1]
        if 'banner_img' in request.data:
            profile_data['banner_url'] = request.data['banner_img']
            profile_data['banner_url'].name = str(request.user.id) + '.' + profile_data['banner_url'].name.split('.')[-1]

        profile_data['name'] = request.data['name']
        profile_data['bio'] = request.data['bio']

        profile_serializer = serializers.ProfileSerializer(profile, data=profile_data, partial=True) 
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)

class SignOutView(views.APIView):
    # only logged in user can log out 
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request): 
        logout(request) 
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
        
class DashboardView(views.APIView): 
    # only logged in user can view dashboard
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request): 
        user_serializer = serializers.UserSerializer(request.user) 
        profile = request.user.profile
        profile_serializer = serializers.ProfileSerializer(profile)
        data = dict(user_serializer.data, **profile_serializer.data)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.profile
        data = {}        
        if 'profile_img' in request.data:
            data['profile_url'] = request.data['profile_img'] 
            # rename 
            data['profile_url'].name = str(request.user.get_username()) + '.' + data['profile_url'].name.split('.')[-1]
        if 'banner_img' in request.data:
            data['banner_url'] = data['banner_img']
            data['banner_url'].name = str(request.user.get_username()) + '.' + data['banner_url'].name.split('.')[-1]

        data['name'] = request.data['name']
        data['bio'] = request.data['bio']
       
        profile_serializer = serializers.ProfileSerializer(profile, data=data, partial=True) 
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserInfoView(views.APIView): 
    # only logged in user can view dashboard
    permission_classes = (permissions.AllowAny, )

    def get(self, request): 
        try:
            if 'id' in request.GET:
                user_id = request.GET['id']
                user = User.objects.get(id=user_id)
            else:
                username = request.GET['username']
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = serializers.UserSerializer(user) 
        profile = user.profile
        profile_serializer = serializers.ProfileSerializer(profile)
        data = dict(user_serializer.data, **profile_serializer.data)
        num_followers = len(user.followers.all())
        num_following = len(user.following.all())
        data['fullname'] = data['name']
        del data['name']
        data['num_followers'] = num_followers
        data['num_following'] = num_following
        data['following'] = True if request.user in user.followers.all() else False
        return Response(data, status=status.HTTP_200_OK)




            