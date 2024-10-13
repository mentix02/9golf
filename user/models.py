import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    @property
    def avatar(self) -> str:
        email_encoded = self.email.lower().encode('utf-8')
        email_hash = hashlib.sha256(email_encoded).hexdigest()

        return f'https://www.gravatar.com/avatar/{email_hash}'
