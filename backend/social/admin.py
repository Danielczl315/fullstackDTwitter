from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

from .models import Following
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()

class FollowingInline(admin.StackedInline):
    model = Following

class FollowAdmin(admin.ModelAdmin):
    # inlines = [FollowingInline, ]
    list_display = ['__str__', 'user_id', 'following_user_id','created']
    search_fields = ['text', 'user__username']

    class Meta:
        model = User

admin.site.register(Following, FollowAdmin)
