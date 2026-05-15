from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuarios(AbstractUser):
    
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name}"