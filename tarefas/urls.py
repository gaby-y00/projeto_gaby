from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/criar', views.criar_tarefa, name='criar_tarefa'),
    path('categoria/<str:nome_categoria>/', views.categoria_filtro, name='categoria'),

    path('excluir/<int:id>/', views.excluir_tarefa, name='excluir_tarefa'),
    path('tarefa/<int:id>/', views.detalhar_tarefa, name='detalhar_tarefa'),
    path('editar/<int:id>/', views.editar_tarefa, name='editar_tarefa'),
    path('concluir/<int:id>/', views.concluir_tarefa, name='concluir_tarefa'),
    path('mudar-plano/', views.mudar_plano, name='mudar_plano'),
    path('nova-categoria/', views.criar_categoria, name='criar_categoria'),
    path('excluir-categoria/<int:id>/', views.excluir_categoria, name='excluir_categoria'),
]