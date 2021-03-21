import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User Model
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_employee(self):
        if self.groups.filter(name='employee').exists():
            return True
        return False

    @property
    def is_admin(self):
        if self.groups.filter(name='admin').exists():
            return True
        return False
