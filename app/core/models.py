from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves new users """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=email.lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """creates and saves a new superuser"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class TagModel(models.Model):
    """Tag to be used for users, each user can have multiple tags"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.name
