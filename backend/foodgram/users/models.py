# Create your models here.
from django.contrib.auth.models import AbstractUser  # PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have am email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()
  
        return user

class UserAccount(AbstractUser):
    # ADMIN = "admin"
    # MODERATOR = "moderator"
    # USER = "user"
    # ROLES = [
    #     (ADMIN, ADMIN),
    #     (MODERATOR, MODERATOR),
    #     (USER, USER),
    # ]
    #username = models.CharField(
    #     max_length=150, null=False, blank=False, unique=True
    # )
    email = models.EmailField(
        max_length=254, unique=True, null=False, blank=False
    )
    name = models.CharField(max_length=150, blank=True)
    # first_name = models.CharField(max_length=150, blank=True)
    # last_name = models.CharField(max_length=150, blank=True)
    #password = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserAccountManager()
    # bio = models.TextField(blank=True)
    # role = models.CharField(max_length=20, choices=ROLES, default=USER)
    # confirmation_code = models.CharField(
    #     max_length=150, blank=False, null=True
    # )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("name",)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name
