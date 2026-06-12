from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):
    confirmation_code = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = str(
                random.randint(100000, 999999)
            )
        super().save(*args, **kwargs)