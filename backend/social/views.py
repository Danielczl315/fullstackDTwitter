import random 

from rest_framework import permissions, status, views
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError 

from .models import Following
from django.contrib.auth import get_user_model

User = get_user_model() 

class UserFollowingView(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request): 
        user = request.user
        try:
            following_user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({'details': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        Following.objects.create(user_id=user, following_user_id=following_user)
        return Response(None, status=status.HTTP_201_CREATED)

    def delete(self, request): 
        user = request.user
        try:
            following_user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({'details': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST) 
        # get relation
        try:
            relation = Following.objects.get(user_id=user, following_user_id=following_user)  
        except Following.DoesNotExist:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)  
        relation.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UseRecommendationView(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request): 
        user = request.user
        following = user.following 
        accounts = list(User.objects.all())
        num = request.GET['num']
        # change 3 to how many random items you want
        if not num:
            suggestions = random.sample(accounts, 10) 
        else: 
            suggestions = random.sample(accounts, num) 
        
        
