from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    address = models.TextField()
    nickname = models.CharField(max_length=100)
    introduction = models.CharField(max_length=300)
    image = models.ImageField(upload_to='profile/%Y%m%d', blank=True)
    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
    )