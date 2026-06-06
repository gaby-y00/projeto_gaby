from django.db import models
from usuarios.models import Usuarios
from django.conf import settings
# Create your models here.

class Perfil(models.Model):
    PLANOS_CHOICES = [
        ('free', 'Gratuito'),
        ('premium', 'Premium Pro'),
    ]
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    plano = models.CharField(max_length=20, choices=PLANOS_CHOICES, default='free')

    def __str__(self):
        return f"{self.usuario.username} - {self.get_plano_display()}"
    
class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome


class Tarefa(models.Model):

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
    categoria = models.CharField(max_length=50)
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE)
    recorrencia = models.CharField(max_length=20, choices=RECORRENCIA_CHOICES, default='nao_repete')
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.categoria} - {self.prioridade}"