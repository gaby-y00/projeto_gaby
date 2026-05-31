from django.db import models
from usuarios.models import Usuarios
from django.conf import settings
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

    RECORRENCIA_CHOICES = [
        ('nao_repete', 'Não se repete (Única)'),
        ('diaria', 'Todos os dias'),
        ('semanal', 'Toda semana'),
        ('mensal', 'Todo mês'),
    ]
            
    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA)
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE)
    recorrencia = models.CharField(max_length=20, choices=RECORRENCIA_CHOICES, default='nao_repete')
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.categoria} - {self.prioridade}"