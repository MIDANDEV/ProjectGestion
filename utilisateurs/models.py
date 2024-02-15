from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class Userprofile(models.Model):
    User = settings.AUTH_USER_MODEL
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ImageField(default='profile.png', upload_to='profile_images')
    pays = models.CharField(max_length=50, blank=True)
    ville = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=10, blank=True)


    def __int__(self):
        return self.user.name





class User(AbstractUser):
    chef_projet=models.BooleanField(default=False)
    gestionnaire_financier=models.BooleanField(default=False)
    porteur_projet=models.BooleanField(default=False)
    membre_regie= models.BooleanField(default=True)
