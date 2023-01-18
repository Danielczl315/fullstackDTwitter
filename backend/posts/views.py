from rest_framework import permissions, status, views
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError 

from . import serializers, pagination

from .models import Post, Like, Reply
from django.contrib.auth import get_user_model

# Create your views here.
class PostView(views.APIView): 

    def get_permissions(self): 
        if self.request.method == 'GET':
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def post(self, request): 
        user = request.user 
        post_serializer = serializers.PostSerializer(data=request.data)
        # check if content exceeds limit
        try:
            post_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({'detail': 'Invalid content'}, status=status.HTTP_400_BAD_REQUEST)
        # create entry
        if 'media' in request.data:
            post = Post(user=user, text=post_serializer.data['text'], media=request.data['media'] )
        else:
            post = Post(user=user, text=post_serializer.data['text'])
        post.save() 
        return Response(None, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        user, post_id = request.user, request.data['post_id']
        # get post
        try:
            post = Post.objects.get(id=post_id)
            # check if the request is valid 
            if user != post.user:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)  
        except Post.DoesNotExist:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)  
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get(self, request): 
        # param is incorrect
        # return Response(None, status=status.HTTP_400_BAD_REQUEST)  
        # TODO: this should be the correct logic, (get post by id)
        post_id = request.GET['post_id']
        post = Post.objects.get(id=post_id) 
        username = post.user.username 
        serialized = serializers.GetPostSerializer(post)
        # we need to check on the frontend if user name is consistent 
        username_info = {'username': username }
        data = dict(serialized.data, **username_info)
        return Response(data, status=status.HTTP_200_OK)


class PostFromUserView(views.APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        username = request.GET['username']
        User = get_user_model()
        try:
            user = User.objects.get(username=username) 
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        posts = user.post_set.all().order_by('-created_at')
        # pagination
        paginator = pagination.StandardResultsSetPagination() 
        page = paginator.paginate_queryset(posts, request)
        # serilaize 
        serializer = serializers.GetPostSerializer
        serialized = serializer(page, many=True)
        json_representation = JSONRenderer().render(serialized.data)
        # Response(json_representation, status=status.HTTP_200_OK)
        return paginator.get_paginated_response(json_representation)

class LikeView(views.APIView):

    def get_permissions(self): 
        if self.request.method == 'GET':
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def post(self, request):
        # add a like  
        user = request.user  
        post_id = request.data['post_id']  
        post = Post.objects.get(id=post_id) 
        # add the user
        post.likes.add(user)
        return Response(None, status=status.HTTP_201_CREATED)

    def delete(self, request):
        # remove a like 
        user = request.user 
        post_id = request.data['post_id']
        post = Post.objects.get(id=post_id) 
        # remove 
        post.likes.remove(user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get(self, request): 
        # return liked count 
        post_id = request.GET['post_id'] 
        post = Post.objects.get(id=post_id) 
        num_likes = len(post.likes)
        return Response(str(num_likes), status=status.HTTP_200_OK)

class LikedByView(views.APIView): 
    permission_classes = (permissions.AllowAny, )

    def get(self, request): 
        # get detailed liked info 
        post_id = request.GET['post_id'] 
        post = Post.objects.get(id=post_id) 
        likes = Like.objects.get(post=post).order_by('-timestamp')
        data = [] 
        for like in likes: 
            info = {}
            info['user_id'] = like.user.id 
            info['username'] = like.user.username
            info['profile_url'] = like.user.profile_url 
            info['bio'] = like.user.bio
            info['timestamp'] = like.timestamp  
            data.append(info)
        return Response(str(data), status=status.HTTP_200_OK) 

class PostStatsView(views.APIView): 
    permission_classes = (permissions.AllowAny, ) 
    
    def get(self, request): 
        post_id = request.GET['post_id'] 
        user = request.user 
        try:
            post = Post.objects.get(id=post_id) 
        except Post.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            likes = post.likes.all()
        except Like.DoesNotExist: 
            likes = []
        
        replies = post.reply_set.all()
        data = {
            'like_count': len(likes),
            'has_user_liked': False,
            'reply_count': len(replies)
        }
        return Response(data, status=status.HTTP_200_OK)

class PostStatsUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request): 
        post_id = request.GET['post_id'] 
        user = request.user 
        try:
            post = Post.objects.get(id=post_id) 
        except Post.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            likes = post.likes.all()
        except Like.DoesNotExist: 
            likes = []
        
        has_user_liked = user in likes 
        replies = post.reply_set.all()
        # return num likes this post got and user info 
        data = {
            'like_count': len(likes),
            'has_user_liked': has_user_liked,
            'reply_count': len(replies)
        }
        return Response(data, status=status.HTTP_200_OK)

class ReplyView(views.APIView):

    def get_permissions(self): 
        if self.request.method == 'GET':
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def post(self, request): 
        user = request.user 
        serializer = serializers.ReplySerializer(data=request.data)
        # check if content exceeds limit
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({'detail': 'Invalid content'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=request.data['post_id']) 
        except Post.DoesNotExist:
            return Response({'detail': 'Invalid post id'}, status=status.HTTP_400_BAD_REQUEST)
        # create entry
        if 'media' in request.data:
            reply = Reply(user=user, replying_to=post, text=serializer.data['text'], media=request.data['media'] )
        else:
            reply = Reply(user=user, replying_to=post, text=serializer.data['text'])
        reply.save() 
        return Response(None, status=status.HTTP_201_CREATED)

    def get(self, request):
        post_id = request.GET['id'] 
        post = Post.objects.get(id=post_id) 
        replies = post.reply_set.all().order_by('-created_at')
        serialized = serializers.GetReplySerializer(replies, many=True)
        json_representation = JSONRenderer().render(serialized.data)
        return Response(json_representation, status=status.HTTP_200_OK)

class ReplyLikeView(views.APIView):

    def get_permissions(self): 
        if self.request.method == 'GET':
            return (permissions.AllowAny(), )
        return (permissions.IsAuthenticated(), )

    def post(self, request):
        # add a like  
        user = request.user  
        reply_id = request.data['reply_id']  
        reply = Reply.objects.get(id=reply_id) 
        # add the user
        reply.likes.add(user)
        return Response(None, status=status.HTTP_201_CREATED)

    def delete(self, request):
        # remove a like 
        user = request.user 
        reply_id = request.data['reply_id']  
        reply = Reply.objects.get(id=reply_id) 
        # remove 
        reply.likes.remove(user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get(self, request): 
        # return liked count 
        reply_id = request.data['reply_id']  
        reply = Post.objects.get(id=reply_id)
        num_likes = len(reply.likes)
        return Response(str(num_likes), status=status.HTTP_200_OK)


class ReplyStatsView(views.APIView): 
    permission_classes = (permissions.AllowAny, ) 
    
    def get(self, request): 
        reply_id = request.GET['post_id'] 
        try:
            reply = Reply.objects.get(id=reply_id) 
        except Reply.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            likes = reply.likes.all()
        except Like.DoesNotExist: 
            likes = []

        data = {
            'like_count': len(likes),
            'has_user_liked': False
        }
        return Response(data, status=status.HTTP_200_OK)

class ReplyStatsUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request): 
        reply_id = request.GET['reply_id'] 
        user = request.user 
        try:
            reply = Reply.objects.get(id=reply_id) 
        except Reply.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        try:
            likes = reply.likes.all()
        except Like.DoesNotExist: 
            likes = []
        
        has_user_liked = user in likes 
        # return num likes this post got and user info 
        data = {
            'like_count': len(likes),
            'has_user_liked': has_user_liked,
        }
        return Response(data, status=status.HTTP_200_OK)