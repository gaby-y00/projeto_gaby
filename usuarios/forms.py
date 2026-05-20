from django import forms
from .models import Usuarios

class CadastroForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    # Em forms.Form, declaramos os campos diretamente, sem "class Meta"
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput() # Continua escondendo a senha com os pontinhos
    )