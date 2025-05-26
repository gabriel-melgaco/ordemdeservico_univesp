# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemDeServico
from .forms import OrdemDeServicoForm, FinalizarOrdemForm, AtualizarStatusCompraForm, ExecutarOrdemForm
from django.utils.dateparse import parse_date
from django.contrib.auth.forms import UserCreationForm
from functools import wraps
from django.contrib.auth import logout
from django.contrib import messages

# Função genérica para verificar grupo Decorador para verificar grupos de usuários
def verifica_grupo(lista_grupos, login_url='/erro_permissao/'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name__in=lista_grupos).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect(login_url)  # Redireciona para a página de erro de permissão
        return _wrapped_view
    return decorator

# Função para criar uma nova ordem de serviço
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def criar_ordem(request):
    numero_ordem_criada = None  # Inicializa a variável para armazenar o número da ordem
    if request.method == 'POST':
        form = OrdemDeServicoForm(request.POST)
        if form.is_valid():
            ordem_criada = form.save()  # Salva a ordem de serviço
            numero_ordem_criada = ordem_criada.id  # Obtém o número da ordem gerada
            messages.success(request, 'Usuário criado com sucesso!')
            return render(request, 'criar_ordem.html', {
                'form': OrdemDeServicoForm(),  # Envia um novo formulário vazio
                'numero_ordem_criada': numero_ordem_criada  # Passa o número da ordem para o template
            })
    else:
        form = OrdemDeServicoForm()
    return render(request, 'criar_ordem.html', {'form': form, 'numero_ordem_criada': numero_ordem_criada})

# Função para listar todas as ordens de serviço
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def listar_ordens(request):
    ordens = OrdemDeServico.objects.all()
    return render(request, 'listar_ordens.html', {'ordens': ordens})

# Função para detalhar uma ordem específica
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def detalhar_ordem(request, pk):
    ordem = get_object_or_404(OrdemDeServico, pk=pk)
    return render(request, 'detalhar_ordem.html', {'ordem': ordem})

# Função para executar uma ordem de serviço
@verifica_grupo(['Administrador', 'Tecnico'], login_url='/erro_permissao/')
def executar_ordem(request, pk):
    ordem = get_object_or_404(OrdemDeServico, pk=pk)
    if request.method == 'POST':
        form = ExecutarOrdemForm(request.POST, instance=ordem)
        if form.is_valid():
            ordem = form.save(commit=False)  # Salva os dados do formulário
            ordem.status = 'Execução'  # Atualiza o status
            ordem.save()
            return redirect('listar_ordens')  # Redireciona para a listagem de ordens
        else:
            print(form.errors)  # Depuração: exibe os erros do formulário, se houver
    else:
        form = ExecutarOrdemForm(instance=ordem)

    return render(request, 'executar_ordem.html', {'form': form, 'ordem': ordem})

# Função para finalizar uma ordem de serviço
@verifica_grupo(['Administrador', 'Tecnico'], login_url='/erro_permissao/')
def finalizar_ordem(request, pk):
    ordem = get_object_or_404(OrdemDeServico, pk=pk)

    if request.method == 'POST':
        form = FinalizarOrdemForm(request.POST, instance=ordem)
        if form.is_valid():
            ordem = form.save(commit=False)
            ordem.status = 'Finalizada'  # Atualiza o status para Finalizada
            ordem.save()
            return redirect('listar_ordens')  # Redireciona para a listagem de ordens
    else:
        form = FinalizarOrdemForm(instance=ordem)

    return render(request, 'finalizar_ordem.html', {'form': form, 'ordem': ordem})

# Função para listar ordens que possuem materiais pendentes de compra
@verifica_grupo(['Administrador', 'Compras'], login_url='/erro_permissao/')
def listar_compras(request):
    compras = OrdemDeServico.objects.filter(possui_material=False, material_necessario__isnull=False).exclude(material_necessario='') 
    return render(request, 'listar_compras.html', {'compras': compras})

# Função para atualizar o status de uma compra
@verifica_grupo(['Administrador', 'Compras'], login_url='/erro_permissao/')
def atualizar_compra(request, pk):
    ordem = get_object_or_404(OrdemDeServico, pk=pk)
    if request.method == 'POST':
        form = AtualizarStatusCompraForm(request.POST, instance=ordem)
        if form.is_valid():
            form.save()
            return redirect('listar_compras')  # Redireciona para a lista de compras
    else:
        form = AtualizarStatusCompraForm(instance=ordem)
    return render(request, 'atualizar_compra.html', {'form': form, 'ordem': ordem})

# Função para buscar uma ordem de serviço pelo número
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def buscar_por_numero(request):
    numero_ordem = request.GET.get('numero_ordem')
    ordem = None
    if numero_ordem:
        ordem = OrdemDeServico.objects.filter(id=numero_ordem).first()
    return render(request, 'buscar_por_numero.html', {'ordem': ordem})

# Função para filtrar ordens por período
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def filtrar_por_periodo(request):
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    ordens = []
    if inicio and fim:
        data_inicio = parse_date(inicio)
        data_fim = parse_date(fim)
        ordens = OrdemDeServico.objects.filter(data_criacao__range=(data_inicio, data_fim))
    return render(request, 'filtrar_por_periodo.html', {'ordens': ordens})

# Funções para exibir páginas iniciais
def home(request):
    return render(request, 'home.html')

@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def home_ordem(request):
    return render(request, 'home_ordem.html')

@verifica_grupo(['Administrador', 'Compras'], login_url='/erro_permissao/')
def home_compras(request):
    return render(request, 'home_compras.html')

@verifica_grupo(['Administrador'], login_url='/erro_permissao/')
def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registrar.html', {'form': form})

# View para a página de erro de permissão
def erro_permissao(request):
    return render(request, 'erro_permissao.html')

def logout_customizado(request):
    logout(request)  # Realiza o logout
    messages.success(request, "Logout realizado com sucesso!")  # Adiciona a mensagem de sucesso
    return redirect('home')  # Redireciona para a página inicia

def about(request):
    return render(request, 'about.html')
