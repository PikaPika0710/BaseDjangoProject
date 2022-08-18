from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models

from api_base.models import TimeStampedModel
from .Role import Role


class Account(AbstractUser, TimeStampedModel):
    objects = UserManager()
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = "account"
        ordering = ('date_joined',)
