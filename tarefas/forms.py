from django import forms
from .models import Tarefa

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'categoria', 'prioridade', 'recorrencia', 'descricao', 'data']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }