import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models

# Генерация реферального кода
def generate_referral_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    auth_code = models.CharField(max_length=4, blank=True, null=True)
    referral_code = models.CharField(max_length=6, unique=True, default=generate_referral_code)
    other_code = models.CharField(max_length=6, blank=True, null=True)

    # Генерация кода аутентификации
    def generate_auth_code(self):
        auth_code = str(random.randint(1000, 9999))
        self.auth_code = auth_code
        self.save()
