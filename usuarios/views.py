from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from .forms import CadastroForm, LoginForm
from .models import Usuarios

# Create your views here.

def cadastro (request):

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            if usuario is not None:
                usuario.password = make_password(usuario.password)
                usuario.save()
                login(request, usuario)
                return redirect('home')
    else:
        form = CadastroForm()
    context = {
        'form': form
    }
    return render(request, 'usuarios/cadastro.html', context)



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email_digitado = form.cleaned_data.get('email')
            password_digitada = form.cleaned_data.get('password')
            
            try:
                usuario_encontrado = Usuarios.objects.get(email=email_digitado)
                
                usuario = authenticate(
                    request, 
                    username=usuario_encontrado.username, 
                    password=password_digitada
                )
                
                if usuario is not None:
                    login(request, usuario)
                    return redirect('home')
                else:
                    form.add_error(None, "Senha incorreta.")
                    
            except Usuarios.DoesNotExist:
                form.add_error(None, "E-mail não cadastrado.")
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'usuarios/login.html', context)