from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # 1. IMPORTANTE: Importe o protetor de tela
from .models import Tarefa
from .forms import TarefaForm
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    # 1. O usuário está logado?
    if request.user.is_authenticated:
        # Se sim, busca apenas as tarefas QUE PERTENCEM A ELE
        lista_de_tarefas = Tarefa.objects.filter(usuario=request.user)
        
        # === AS TRÊS LINHAS DA BUSCA ENTRAM AQUI: ===
        termo_pesquisa = request.GET.get('search')
        if termo_pesquisa:
            lista_de_tarefas = lista_de_tarefas.filter(titulo__icontains=termo_pesquisa)
        # ============================================
        
        context = {
            'tarefas': lista_de_tarefas
        }
        # Renderiza a página interna (o painel de tarefas)
        return render(request, 'tarefas/home.html', context)
        
    # 2. Se o usuário NÃO estiver logado:
    else:
        # Renderiza a página pública de boas-vindas
        return render(request, 'tarefas/landing.html')
    

""" ------------------------------------------------------------- """

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

""" ------------------------------------------------------------- """

def categoria_filtro(request, nome_categoria):
    # Garante que o usuário está logado
    if not request.user.is_authenticated:
        return redirect('login')
        
    # Filtra as tarefas: devem ser do usuário logado E da categoria clicada
    # O .order_by('-prioridade') assume que você tem um campo de prioridade no seu modelo
    lista_filtrada = Tarefa.objects.filter(
        usuario=request.user, 
        categoria=nome_categoria
    ).order_by('-prioridade') # O sinal de menos (-) faz vir as maiores prioridades primeiro
    
    context = {
        'tarefas': lista_filtrada,
        'categoria_atual': nome_categoria
    }
    
    # Reutilizamos o próprio home.html! Não precisa criar outro arquivo.
    return render(request, 'tarefas/home.html', context)



""" ------------------------------------------------------------- """


def excluir_tarefa(request, id):
    # 1. Garante que o usuário está logado
    if not request.user.is_authenticated:
        return redirect('login')
        
    # 2. Busca a tarefa pelo ID, garantindo que ela pertence a este usuário logado
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    # 3. Se o usuário confirmou a exclusão (método POST)
    if request.method == 'POST':
        tarefa.delete() # Apaga do banco de dados
        return redirect('tarefas:home') # Volta pro painel
        
    # 4. Se ele apenas clicou no botão, mostra uma tela perguntando "Tem certeza?"
    return render(request, 'tarefas/excluir_tarefa.html', {'tarefa': tarefa})


""" ------------------------------------------------------------- """


def detalhar_tarefa(request, id):
    # 1. Garante que o usuário está logado
    if not request.user.is_authenticated:
        return redirect('login')
        
    # 2. Busca a tarefa do usuário logado pelo ID
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    # 3. Envia os dados da tarefa para a nova página
    return render(request, 'tarefas/detalhar_tarefa.html', {'tarefa': tarefa})