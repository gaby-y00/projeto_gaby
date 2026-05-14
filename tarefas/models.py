from django.db import models
from usuarios.models import Usuarios
# Create your models here.

class Tarefa(models.Model):

    CATEGORIA = [
        ('Estudo', 'Estudo'),
        ('Pessoal', 'Pessoal'),
        ('Financeiro', 'Financeiro'),
        ('Compromisso', 'Compromisso'),
    ]

    PRIORIDADE = [
        ('U','Urgente'),
        ('M','Médio'),
        ('F','Flexível'),
    ]

    TIPO = [
        ('F','Fixa'),
        ('T','Temporária'),
    ]

    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA)
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE)
    tipo = models.CharField(max_length=1, choices=TIPO)
    descricao = models.TextField()
    data = models.DateField()
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.categoria} - {self.prioridade}"