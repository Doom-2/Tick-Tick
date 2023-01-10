from django.contrib.auth.models import AbstractUser
from core.managers import UserManager


class User(AbstractUser):
    objects = UserManager()

    USERNAME_FIELD = 'username'
