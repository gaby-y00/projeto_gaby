from django.contrib import admin
from .models import Tarefa, Categoria, Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'plano')
    list_filter = ('plano',)  
    search_fields = ('usuario__username',) 

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'prioridade', 'concluida')
    list_filter = ('concluida', 'prioridade')
    search_fields = ('titulo', 'usuario__username')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario')
    search_fields = ('nome', 'usuario__username')