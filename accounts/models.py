from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.utils import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=125, unique=True)
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    objects = CustomUserManager()
