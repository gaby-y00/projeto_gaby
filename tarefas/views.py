from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tarefa, Perfil, Categoria
from .forms import TarefaForm
import json
from datetime import date

def home(request):
    if request.user.is_authenticated:
        lista_de_tarefas = Tarefa.objects.filter(usuario=request.user)

        try:
            plano_usuario = request.user.perfil.plano
        except:
            plano_usuario = 'free'
            
        if plano_usuario == 'free':
            categorias_padrao = ['Estudo', 'Pessoal', 'Financeiro', 'Compromisso']
            lista_de_tarefas = lista_de_tarefas.filter(categoria__in=categorias_padrao)

        tarefas_calendario = []
    
        for t in lista_de_tarefas.filter(data__isnull=False, concluida=False):
            tarefas_calendario.append({
                'data': t.data.strftime('%Y-%m-%d'),
                'prioridade': t.prioridade,
                'titulo': t.titulo
            })

        tarefas_json = json.dumps(tarefas_calendario)
        termo_pesquisa = request.GET.get('search')

        if termo_pesquisa:
            lista_de_tarefas = lista_de_tarefas.filter(titulo__icontains=termo_pesquisa)
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
            'data_filtrada': data_filtrada_display,
            'hoje': date.today()
        }
        return render(request, 'tarefas/home.html', context)
    else:
        return render(request, 'tarefas/landing.html')

@login_required 
def criar_tarefa(request):
    try:
        plano_usuario = request.user.perfil.plano
    except:
        plano_usuario = 'free'

    total_tarefas = Tarefa.objects.filter(usuario=request.user).count()

    if request.method == 'POST':
        
        if plano_usuario == 'free' and total_tarefas >= 10:
            context = {
                'form': TarefaForm(), 
                'erro_limite': 'Você atingiu o limite de 10 tarefas do plano Gratuito. Exclua tarefas antigas ou faça upgrade para o Premium.',
                'plano_usuario': plano_usuario,
                'total_tarefas': total_tarefas
            }
            return render(request, 'tarefas/criar_tarefa.html', context)
        
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        prioridade = request.POST.get('prioridade')
        data = request.POST.get('data')
        
        if plano_usuario == 'free':
            recorrencia = 'nao_repete'
        else:
            recorrencia = request.POST.get('recorrencia')

        if data == '':
            data = None
        
        Tarefa.objects.create(
            titulo=titulo,                      
            descricao=descricao,
            categoria=categoria,
            prioridade=prioridade,
            data=data,
            recorrencia=recorrencia,
            usuario=request.user
        )
        return redirect('home')
            
    else:
        form = TarefaForm()

    context = {
        'form': form,
        'plano_usuario': plano_usuario,
        'total_tarefas': total_tarefas
    }
    return render(request, 'tarefas/criar_tarefa.html', context)


def categoria_filtro(request, nome_categoria):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        plano = request.user.perfil.plano
    except:
        plano = 'free'

    categorias_padrao = ['Estudo', 'Pessoal', 'Financeiro', 'Compromisso']
    
    if plano == 'free' and nome_categoria not in categorias_padrao:
        return redirect('home')

    lista_filtrada = Tarefa.objects.filter(
        usuario=request.user, 
        categoria=nome_categoria
    ).order_by('-prioridade')
    
    context = {
        'tarefas': lista_filtrada,
        'categoria_atual': nome_categoria,
        'hoje': date.today()
    }
    
    return render(request, 'tarefas/home.html', context)


def excluir_tarefa(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    if request.method == 'POST':
        tarefa.delete()
        return redirect('home')
        
    return render(request, 'tarefas/excluir_tarefa.html', {'tarefa': tarefa})


def detalhar_tarefa(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    return render(request, 'tarefas/detalhar_tarefa.html', {'tarefa': tarefa})


@login_required
def editar_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)

    try:
        plano_usuario = request.user.perfil.plano
    except:
        plano_usuario = 'free'

    categorias_padrao = ['Estudo', 'Pessoal', 'Financeiro', 'Compromisso']
    categorias_personalizadas = []
    
    if plano_usuario == 'premium':
        categorias_personalizadas = list(Categoria.objects.filter(usuario=request.user).values_list('nome', flat=True))
        
    todas_categorias = categorias_padrao + categorias_personalizadas
    if tarefa.categoria not in todas_categorias:
        todas_categorias.append(tarefa.categoria)

    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.categoria = request.POST.get('categoria')
        tarefa.prioridade = request.POST.get('prioridade')
        
        if plano_usuario == 'free':
            tarefa.recorrencia = 'nao_repete'
        else:
            tarefa.recorrencia = request.POST.get('recorrencia')
            
        tarefa.descricao = request.POST.get('descricao')
        tarefa.data = request.POST.get('data') or None 
        tarefa.save()
        return redirect('home')

    return render(request, 'tarefas/editar_tarefa.html', {
        'tarefa': tarefa,
        'categorias': todas_categorias,
        'plano_usuario': plano_usuario 
    })


def concluir_tarefa(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    tarefa = get_object_or_404(Tarefa, id=id, usuario=request.user)
    
    tarefa.concluida = not tarefa.concluida
    tarefa.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def mudar_plano(request):
    if request.method == 'POST':
        perfil, created = Perfil.objects.get_or_create(usuario=request.user)
        
        if perfil.plano == 'free':
            perfil.plano = 'premium'
        else:
            perfil.plano = 'free'
            
        perfil.save()
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def criar_categoria(request):
    try:
        if request.user.perfil.plano == 'free':
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    except:
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    if request.method == 'POST':
        nome = request.POST.get('nome_categoria')
        if nome:
            Categoria.objects.create(nome=nome, usuario=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def excluir_categoria(request, id):
    if request.user.perfil.plano != 'premium':
        return redirect('home')
    categoria = get_object_or_404(Categoria, id=id, usuario=request.user)
    nome_da_categoria_deletada = categoria.nome
    categoria.delete()
    Tarefa.objects.filter(
        usuario=request.user, 
        categoria=nome_da_categoria_deletada
    ).update(categoria='Pessoal')
    return redirect(request.META.get('HTTP_REFERER', 'home'))