# 🎯 AGENDA FLUIDA

## Objetivo e Problema que Busca Resolver
O objetivo deste sistema é ser um gerenciador de tarefas inteligente e adaptável. O problema principal que ele resolve é a desorganização pessoal e a poluição visual dos aplicativos de produtividade tradicionais. Ao combinar uma lista de afazeres com uma visualização de calendário dinâmico, o sistema permite que o usuário foque nas pendências do dia, não se perca em tarefas vencidas e consiga categorizar suas demandas de forma eficiente.

---

## 👥 Tipos de Usuários Suportados e Permissões
O sistema trabalha com autenticação e possui uma arquitetura baseada em planos de assinatura (SaaS). Atualmente, suporta dois tipos de usuários finais, além do administrador do sistema:

### 1. Usuário Padrão (Plano Free)
*(É o usuário recém-cadastrado na plataforma)*
* **O que pode fazer:** Criar até 10 tarefas, editar, concluir, excluir e visualizar detalhes. Pode navegar pelo calendário interativo e organizar suas tarefas usando as 4 categorias fixas do sistema (Estudo, Pessoal, Financeiro e Compromissos).

### 2. Usuário Premium (Plano Pro)
*(É o usuário que realizou o upgrade da conta)*
* **O que pode fazer:** Tem acesso ilimitado à criação de tarefas. Pode criar categorias (tags) 100% personalizadas para organizar suas tarefas. Pode excluir essas categorias, pode deixar as tarefas com a frequência que desejar (todos os dias, toda semana ou todo mês) e possui um painel lateral dinâmico. Caso cancele a assinatura, o sistema protege seus dados, ocultando as categorias premium sem excluí-las.

### 3. Administrador (Superuser)
* **O que pode fazer:** Acessar o painel `/admin` do Django, gerenciar os cadastros e alterar manualmente o nível de permissão (Free/Premium) dos perfis dos usuários, além de ter controle total sobre as categorias e tarefas cadastradas no banco de dados.

---

## 🚀 Como Instalar e Executar o Projeto (Ambiente de Testes)

Siga rigorosamente os passos abaixo para clonar, configurar e rodar o projeto localmente.

**1. Clonar o Repositório**
```bash
git clone https://github.com/gaby-y00/projeto_gaby.git

# Em seguida, entre na pasta principal do projeto:
cd projeto_gaby

# 2. Criar e Ativar o Ambiente Virtual (venv):
# No Windows:
python -m venv venv
venv\Scripts\activate

# ------------------- #

# No Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# 3. Instalar as Dependências:
pip install django

# 4. Executar as Migrações (Banco de Dados):
python manage.py makemigrations
python manage.py migrate

```
# Dados Iniciais para Testes (Carga Automatizada)
O sistema depende de relacionamentos entre Usuários e Perfis. Para facilitar a avaliação, preparei um script que insere usuários com planos diferentes e tarefas prontas (incluindo testes de tarefas atrasadas).

```bash
# Abra o Shell interativo do Django:
python manage.py shell

# Copie todo o bloco de código abaixo, cole dentro do terminal Shell:
from usuarios.models import Usuarios
from tarefas.models import Perfil, Tarefa, Categoria
from datetime import date, timedelta

# 1. Criando Usuário Free de Teste
user_free, _ = Usuarios.objects.get_or_create(username="teste_free", email="free@teste.com")
user_free.set_password("senha123")
user_free.save()
perfil_free, _ = Perfil.objects.get_or_create(usuario=user_free)
perfil_free.plano = "free"
perfil_free.save()

Tarefa.objects.get_or_create(
    titulo="Estudar para a Prova", categoria="Estudo",
    prioridade="U", data=date.today(), usuario=user_free
)
# Tarefa Atrasada para teste da tag (Pendente)
Tarefa.objects.get_or_create(
    titulo="Pagar conta de Internet", categoria="Financeiro",
    prioridade="U", data=date.today() - timedelta(days=1), usuario=user_free
)

# 2. Criando Usuário Premium de Teste
user_premium, _ = Usuarios.objects.get_or_create(username="teste_premium", email="premium@teste.com")
user_premium.set_password("senha123")
user_premium.save()
perfil_premium, _ = Perfil.objects.get_or_create(usuario=user_premium)
perfil_premium.plano = "premium"
perfil_premium.save()

Categoria.objects.get_or_create(nome="Trabalho", usuario=user_premium)

Tarefa.objects.get_or_create(
    titulo="Reunião Semanal", categoria="Trabalho",
    prioridade="M", data=date.today(), recorrencia="semanal", usuario=user_premium
)

# 3. Criando Administrador
if not Usuarios.objects.filter(username="admin").exists():
    admin_user = Usuarios.objects.create_superuser(username="admin", email="admin@teste.com", password="admin123")
    Perfil.objects.get_or_create(usuario=admin_user, plano="premium")

print("\n=== AMBIENTE POPULADO COM SUCESSO! ===")

# Digite exit() para sair do Shell e inicie o servidor (python manage.py runserver).
exit()
python manage.py runserver
```

# Tour Guiado e Roteiro de Testes
siga este roteiro de testes usando as contas geradas pelo script:

# 1. A Experiência e Limitações do Plano Free
* Acesso: Faça login com `teste_free` | Senha: `senha123`

* **Tag de Atraso Inteligente:** Logo na tela principal, observe a tarefa (`Pagar conta de Internet`). Como a data de vencimento dela está no passado, o sistema aplica automaticamente a tag (`Pendente`) em destaque vermelho. Marque a tarefa como concluída e veja a tag desaparecer imediatamente.

* **Bloqueio de Funcionalidades:** Clique em (`Nova Tarefa`) (ou edite uma existente). Note que o campo de (`Recorrência/Repetição`) está visualmente desabilitado, protegido e sinalizado com a tag de plano Premium.

* **Trava de Quantidade:** O sistema possui um bloqueador ativo: usuários Free só podem possuir um máximo de 10 tarefas cadastradas simultaneamente e não podem criar tags/categorias novas.

# 2. O Poder e Flexibilidade do Plano Premium
* Acesso: Saia da conta Free e faça login com `teste_premium` | Senha: `senha123`

* **Gestão de Categorias:** Observe o menu lateral. O usuário Premium possui um campo exclusivo para criar categorias 100% personalizadas (tente criar uma chamada "Faculdade"). Elas aparecem e podem ser excluídas dinamicamente.

* **Recorrência Liberada:** Vá em (`Nova Tarefa`) e veja que o campo de frequência está totalmente destravado, permitindo criar rotinas diárias, semanais ou mensais.

# 3. O Teste de Ouro: Segurança no Rebaixamento de Plano
Ainda logado na conta `teste_premium`, vamos simular o cancelamento da assinatura para provar a blindagem de dados do sistema:

1. Clique na opção de Gerenciar Plano/Perfil e rebaixe a sua conta para `Free`.

2. **Ocultação de Dados em Tempo Real:** Imediatamente, a categoria customizada `Trabalho` desapareceu do menu. A tarefa `Reunião  Semanal` (que pertencia a ela) sumiu completamente da tela inicial e do calendário. O sistema protege o banco de dados e não deleta suas informações, apenas as oculta por falta de permissão.

3. **Travas Reativadas:** Tente criar uma nova tarefa agora. O limite de 10 tarefas voltou e o campo de recorrência está novamente bloqueado.

4. **O Retorno:** Volte no perfil e mude seu plano novamente para **Premium**. Magicamente, suas categorias personalizadas e todas as tarefas ocultas reaparecem intactas na interface!

### 4. Gestão Administrativa
* Acesso: Acesse `http://127.0.0.1:8000/admin` com login `admin` e senha `admin123`.

* Pelo painel de administração do Django, você pode revisar o banco de dados completo e alterar os níveis de plano diretamente na tabela de Perfis, forçando as regras de negócio a serem aplicadas aos usuários em tempo real.