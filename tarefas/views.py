from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # 1. IMPORTANTE: Importe o protetor de tela
from .models import Tarefa
from .forms import TarefaForm
import json
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    if request.user.is_authenticated:
        lista_de_tarefas = Tarefa.objects.filter(usuario=request.user)

        # === NOVO: BUSCA E FORMATA AS TAREFAS PARA O CALENDÁRIO ===
        tarefas_calendario = []
        # Filtra apenas as tarefas do usuário que possuem uma data preenchida
        for t in lista_de_tarefas.filter(data__isnull=False):
            tarefas_calendario.append({
                'data': t.data.strftime('%Y-%m-%d'),  # Formato padrão: Ano-Mês-Dia
                'prioridade': t.prioridade,
                'titulo': t.titulo
            })

        tarefas_json = json.dumps(tarefas_calendario)

        termo_pesquisa = request.GET.get('search')
        if termo_pesquisa:
            lista_de_tarefas = lista_de_tarefas.filter(titulo__icontains=termo_pesquisa)
        
        # === NOVO: FILTRO POR DATA DO CALENDÁRIO ===
        data_parametro = request.GET.get('data')
        data_filtrada_display = None
        
        if data_parametro:
            lista_de_tarefas = lista_de_tarefas.filter(data=data_parametro)
            try:
                from datetime import datetime
                data_filtrada_display = datetime.strptime(data_parametro, '%Y-%m-%d').strftime('%d/%m/%Y')
            except ValueError:
                data_filtrada_display = data_parametro
        
        context = {
            'tarefas': lista_de_tarefas,
            'tarefas_json': tarefas_json,
            'data_filtrada': data_filtrada_display  # <-- Enviando a data para o HTML
        }
        # Renderiza a página interna (o painel de tarefas)
        return render(request, 'tarefas/home.html', context)
        
    # 2. Se o usuário NÃO estiver logado:
    else:
        # Renderiza a página pública de boas-vindas
        return render(request, 'tarefas/landing.html')
    

""" --------------------------------------------------------------------------------------------------------------- """

@login_required 
def criar_tarefa(request):
    if request.method == 'POST':

        if request.method == 'POST':
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')
            categoria = request.POST.get('categoria')
            prioridade = request.POST.get('prioridade')
            data = request.POST.get('data')
            recorrencia = request.POST.get('recorrencia') # <-- PEGAR O NOVO CAMPO
            if data == '':
                data = None
        
        Tarefa.objects.create(
            titulo=titulo,                      
            descricao=descricao,
            categoria=categoria,
            prioridade=prioridade,
            data=data,
            recorrencia=recorrencia, # <-- SALVAR NO BANCO
            usuario=request.user
        )
        return redirect('home')
            
    else:
        form = TarefaForm()

    context = {
        'form': form
    }
    return render(request, 'tarefas/criar_tarefa.html', context)

""" --------------------------------------------------------------------------------------------------------------- """

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



""" --------------------------------------------------------------------------------------------------------------- """


def excluir_tarefa(request, id):
    # 1. Garante que o usuário está logado
    if not request.user.is_authenticated:
        return redirect('login')
        
    # 2. Busca a tarefa pelo ID, garantindo que ela pertence a este usuário logado
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    # 3. Se o usuário confirmou a exclusão (método POST)
    if request.method == 'POST':
        tarefa.delete() # Apaga do banco de dados
        return redirect('home') # Volta pro painel
        
    # 4. Se ele apenas clicou no botão, mostra uma tela perguntando "Tem certeza?"
    return render(request, 'tarefas/excluir_tarefa.html', {'tarefa': tarefa})


""" --------------------------------------------------------------------------------------------------------------- """


def detalhar_tarefa(request, id):
    # 1. Garante que o usuário está logado
    if not request.user.is_authenticated:
        return redirect('login')
        
    # 2. Busca a tarefa do usuário logado pelo ID
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    # 3. Envia os dados da tarefa para a nova página
    return render(request, 'tarefas/detalhar_tarefa.html', {'tarefa': tarefa})


""" --------------------------------------------------------------------------------------------------------------- """



def editar_tarefa(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    # Busca a tarefa que será editada
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.categoria = request.POST.get('categoria')
        tarefa.prioridade = request.POST.get('prioridade')
        tarefa.recorrencia = request.POST.get('recorrencia') # <-- PEGAR O NOVO CAMPO
    
        # === AJUSTE DA DATA NA EDIÇÃO ===
        nova_data = request.POST.get('data')
        
        # Se mudou para diária ou deixou em branco, a data vira Nula
        if tarefa.recorrencia == 'diaria' or nova_data == '':
            tarefa.data = None
        elif nova_data: # Se ele escolheu uma nova data válida
            tarefa.data = nova_data
            
        tarefa.save()
        return redirect('home')
        
    return render(request, 'tarefas/editar_tarefa.html', {'tarefa': tarefa})
