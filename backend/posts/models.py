from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Post(models.Model):
    # tweet id is default in django db
    # text content same setup as twitter
    text = models.CharField(max_length=280)
    # user_id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # support image only, optional (blank = true)
    media = models.FileField(upload_to='post_media', blank=True, null=True) 
    # created_time  
    created_at = models.DateTimeField(auto_now_add=True)
    # likes 
    likes = models.ManyToManyField(User, related_name="liked_set", blank=True, through="Like")

# Like info 
class Like(models.Model): 
    # user of this like
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # post which this like is on
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    # comment id is defult in django db 
    # replying to which post   
    replying_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    # which user posted this 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # text-content same as post 
    text = models.CharField(max_length=280)
    # optional media field image only, optional (blank = true)
    media = models.FileField(upload_to='reply_media', blank=True, null=True)   
    # likes 
    likes = models.ManyToManyField(User, related_name="reply_liked_set", blank=True, through="ReplyLike") 
    # creation time 
    created_at = models.DateTimeField(auto_now_add=True)

# Reply Like info 
class ReplyLike(models.Model): 
    # user of this like
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # reply which this like is on
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(auto_now_add=True)