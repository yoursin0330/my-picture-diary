from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('User must have an username')
        if not email:
            raise ValueError('User must have an email')
        now = timezone.localtime()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # create_user

    def create_user(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password, False, False, **extra_fields)
    # create_superuser

    def create_superuser(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password, True, True, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD = 'username'
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS =[username, email]

    objects = UserManager()
