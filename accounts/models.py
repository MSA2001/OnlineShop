from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    phone_number = models.CharField(unique=True, max_length=11)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'             # in authentication
    REQUIRED_FIELDS = ['email', 'full_name']        # in creating superuser

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

