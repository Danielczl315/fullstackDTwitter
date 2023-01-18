from django.contrib import admin

from .models import Post, Like, Reply

class LikeAdmin(admin.TabularInline):
    model = Like

class ReplyAdmin(admin.StackedInline):
    model = Reply

class PostAdmin(admin.ModelAdmin):
    inlines = [LikeAdmin, ReplyAdmin]
    list_display = ['__str__', 'user', 'created_at']
    search_fields = ['text', 'user__username']

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
