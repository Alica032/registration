from functools import partial

from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import get_random_string
from django.utils import timezone

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("username", db_index=True, max_length=130, unique=True)
    is_staff = models.BooleanField("is_staff", default=False)
    is_active = models.BooleanField("is_active", default=True)
    phone = models.CharField(
        "phone",
        max_length=16,
        unique=True,
        error_messages={"unique": "Another user with this phone number already exists"},
    )
    email = models.EmailField("email", blank=True, null=True, unique=True)
    is_send_letter = models.BooleanField("letter is send", default=False)

    token = models.CharField(
        max_length=64,
        default=partial(get_random_string, 64)
    )
    created = models.DateTimeField('created', default=timezone.now)


    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        ordering = ("username",)
        verbose_name = "user"
        verbose_name_plural = "users"
