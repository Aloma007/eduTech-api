from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_tutor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({'Tutor' if self.is_tutor else 'Student'})"