from django.contrib import admin
from .models import Tarefa # Importa a sua model de tarefas

# Registra a model para ela aparecer no painel
admin.site.register(Tarefa)