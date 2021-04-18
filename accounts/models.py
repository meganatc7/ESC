from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_active = models.BooleanField(
        default=False,
    )
    email = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=300)
    nickname = models.CharField(max_length=100, unique=True)
    introduction = models.TextField()
    image = models.ImageField(upload_to='profile/%Y%m%d', null=True, blank=True)
    auth = models.CharField(max_length=20, blank=True)
    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
    )