from django.contrib import admin
from .models import Usuarios # Importa a sua model de usuários customizada

# Registra a model de usuários no painel
admin.site.register(Usuarios)