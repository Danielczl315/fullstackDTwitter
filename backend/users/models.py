# django imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# local imports
from .storage import OverwriteStorage
from .utils import generate_nonce
from .validators import validate_username
# Create your models here.

class User(AbstractUser):
    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_username],
        error_messages={
            'unique': _("A user with this username already exists."),
        },
    )
    wallet_address = models.CharField(max_length=42, default='', db_index=True, unique=True)
    nonce = models.CharField(max_length=30, default=generate_nonce)  
    new_user = models.BooleanField(default=True)

    def __str(self):
        return self.username 
 
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=160, default='', blank=True) 
    name = models.CharField(max_length=50, default='')
    profile_url = models.ImageField(default='default.png', upload_to='profile_pics', storage=OverwriteStorage())   
    banner_url = models.ImageField(default='banner_default.png', upload_to='banner_pics', storage=OverwriteStorage())


