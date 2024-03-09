"""
Users models(tables).
"""
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager as BUM
)

from common.models import BaseModel


class BaseUserManager(BUM):

    def create_user(
            self, email, is_active=True, is_admin=False, password=None
    ):
        """Creating normal users with the given email and password."""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active, is_admin=is_admin
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_staff=True,
            password=password,
        )

        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='email address', unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email
