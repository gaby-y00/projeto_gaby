from django.db import models

# Create your models here.

class Usuarios (models.Model):
    nome = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=50)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome}"