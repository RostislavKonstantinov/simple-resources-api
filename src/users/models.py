from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Empty:
    pass


class UserManager(DjangoUserManager):

    def create_user(self, email=None, password=None, **extra_fields):
        return super().create_user(Empty, email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(Empty, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, editable=False)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        kwargs.pop('username', None)
        super().__init__(*args, **kwargs)
