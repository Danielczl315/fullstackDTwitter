from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Profile
# Register your models here.

class ProfileAdmin(admin.StackedInline):
    model = Profile

class CustomUserAdmin(UserAdmin): 
    inlines = [ProfileAdmin]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["wallet_address", "username", "new_user"]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
