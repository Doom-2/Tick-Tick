from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Create user function. Required fields are passed here.
    """

    def _create_user(self, username: str,
                     email: str, password: str,
                     is_staff: bool,
                     is_superuser: bool,
                     **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, email: str = None, password: str = None, **extra_fields):
        return self._create_user(username, email, password, is_staff=False, is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, username: str, email: str, password: str, **extra_fields):
        user = self._create_user(username, email, password, is_active=True, is_staff=True, is_superuser=True,
                                 **extra_fields)
        user.save(using=self._db)
        return user
