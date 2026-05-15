from django.shortcuts import render
from .models import Tarefa
# Create your views here.

def home (request):

    lista_de_tarefas = Tarefa.objects.all()

    context = {
        'tarefas': lista_de_tarefas
    }

    return render (request, 'tarefas/home.html', context)