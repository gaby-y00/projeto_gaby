from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # 1. IMPORTANTE: Importe o protetor de tela
from .models import Tarefa
from .forms import TarefaForm

def home(request):
    if request.user.is_authenticated:
        lista_de_tarefas = Tarefa.objects.filter(usuario=request.user)
    else:
        lista_de_tarefas = Tarefa.objects.none()

    context = {
        'tarefas': lista_de_tarefas
    }
    return render(request, 'tarefas/home.html', context)


@login_required 
def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
            return redirect('home')
            
    else:
        form = TarefaForm()

    context = {
        'form': form
    }
    return render(request, 'tarefas/criar_tarefa.html', context)