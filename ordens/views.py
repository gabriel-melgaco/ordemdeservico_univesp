# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemDeServico
from .forms import (
    OrdemDeServicoForm, FinalizarOrdemForm, AtualizarStatusCompraForm,
    ExecutarOrdemForm, CriarEmpresaForm, RegistrarUsuarioForm
)
from django.utils.dateparse import parse_date
from django.contrib.auth import logout
from django.contrib import messages
from functools import wraps
import logging
import requests

logger = logging.getLogger(__name__)


# Decorador para verificar grupos de usuários
def verifica_grupo(lista_grupos, login_url='/erro_permissao/'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name__in=lista_grupos).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect(login_url)
        return _wrapped_view
    return decorator


# Função para criar uma nova ordem de serviço
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def criar_ordem(request):
    numero_ordem_criada = None
    if request.method == 'POST':
        form = OrdemDeServicoForm(request.POST)
        if form.is_valid():
            ordem_criada = form.save()
            numero_ordem_criada = ordem_criada.id
            messages.success(request, 'Ordem de serviço criada com sucesso!')
            return render(request, 'criar_ordem.html', {
                'form': OrdemDeServicoForm(),
                'numero_ordem_criada': numero_ordem_criada
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
            ordem = form.save(commit=False)
            ordem.status = 'Execução'
            ordem.save()
            return redirect('listar_ordens')
        else:
            logger.warning("Erros no formulário ExecutarOrdem (OS #%s): %s", pk, form.errors)
            messages.error(request, 'Corrija os erros abaixo.')
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
            ordem.status = 'Finalizada'
            ordem.save()
            return redirect('listar_ordens')
    else:
        form = FinalizarOrdemForm(instance=ordem)

    return render(request, 'finalizar_ordem.html', {'form': form, 'ordem': ordem})


# Função para listar ordens com materiais pendentes de compra
# Ordens onde possui_material=False (não tem o material) E material_necessario foi preenchido
@verifica_grupo(['Administrador', 'Compras'], login_url='/erro_permissao/')
def listar_compras(request):
    compras = OrdemDeServico.objects.filter(
        possui_material=False,
        material_necessario__isnull=False
    ).exclude(material_necessario='')
    return render(request, 'listar_compras.html', {'compras': compras})


# Função para atualizar o status de uma compra
@verifica_grupo(['Administrador', 'Compras'], login_url='/erro_permissao/')
def atualizar_compra(request, pk):
    ordem = get_object_or_404(OrdemDeServico, pk=pk)
    if request.method == 'POST':
        form = AtualizarStatusCompraForm(request.POST, instance=ordem)
        if form.is_valid():
            form.save()
            return redirect('listar_compras')
    else:
        form = AtualizarStatusCompraForm(instance=ordem)
    return render(request, 'atualizar_compra.html', {'form': form, 'ordem': ordem})


@verifica_grupo(['Administrador', 'Compras'], login_url='/erro_permissao/')
def consultar_empresa(request):
    if request.method == 'POST':
        form = CriarEmpresaForm(request.POST)
        if form.is_valid():
            cnpj = form.cleaned_data.get('cnpj', '').replace('.', '').replace('/', '').replace('-', '')

            url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                response.raise_for_status()
                dados = response.json()

                if dados.get('status') == 'ERROR':
                    messages.error(request, f"Erro: {dados.get('message', 'Não foi possível consultar o CNPJ.')}")
                else:
                    form = CriarEmpresaForm(initial={
                        'cnpj': dados.get('cnpj', ''),
                        'razao_social': dados.get('nome', ''),
                        'nome_fantasia': dados.get('fantasia', ''),
                        'email': dados.get('email', ''),
                        'telefone': dados.get('telefone', ''),
                        'endereco': dados.get('logradouro', ''),
                        'numero': dados.get('numero', ''),
                        'bairro': dados.get('bairro', ''),
                        'cidade': dados.get('municipio', ''),
                        'estado': dados.get('uf', ''),
                        'cep': dados.get('cep', ''),
                    })
                    messages.success(request, "Dados da empresa carregados com sucesso!")
            except requests.exceptions.Timeout:
                messages.error(request, "A consulta à Receita Federal excedeu o tempo limite. Tente novamente.")
            except requests.exceptions.RequestException as e:
                logger.error("Erro ao consultar ReceitaWS: %s", e)
                messages.error(request, "Erro ao acessar a API da Receita. Tente novamente mais tarde.")
    else:
        form = CriarEmpresaForm()

    return render(request, 'criar_empresa.html', {'form': form})


# Função para buscar uma ordem de serviço pelo número
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def buscar_por_numero(request):
    numero_ordem = request.GET.get('numero_ordem', '').strip()
    ordem = None
    erro = None
    if numero_ordem:
        try:
            pk = int(numero_ordem)
            ordem = OrdemDeServico.objects.filter(id=pk).first()
            if not ordem:
                erro = "Nenhuma ordem encontrada com esse número."
        except ValueError:
            erro = "O número da ordem deve ser um valor numérico."
    return render(request, 'buscar_por_numero.html', {'ordem': ordem, 'erro': erro})


# Função para filtrar ordens por período
@verifica_grupo(['Administrador', 'Usuario', 'Tecnico'], login_url='/erro_permissao/')
def filtrar_por_periodo(request):
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    ordens = []
    erro = None
    if inicio and fim:
        data_inicio = parse_date(inicio)
        data_fim = parse_date(fim)
        if data_inicio is None or data_fim is None:
            erro = "Formato de data inválido. Use o formato AAAA-MM-DD."
        elif data_inicio > data_fim:
            erro = "A data inicial não pode ser posterior à data final."
        else:
            ordens = OrdemDeServico.objects.filter(data_criacao__date__range=(data_inicio, data_fim))
    return render(request, 'filtrar_por_periodo.html', {'ordens': ordens, 'erro': erro})


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
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo = form.cleaned_data.get('grupo')
            if grupo:
                user.groups.add(grupo)
            messages.success(request, f'Usuário "{user.username}" criado com sucesso no grupo "{grupo}".')
            return redirect('registrar')
    else:
        form = RegistrarUsuarioForm()
    return render(request, 'registrar.html', {'form': form})


# View para a página de erro de permissão
def erro_permissao(request):
    return render(request, 'erro_permissao.html')


def logout_customizado(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('home')


def about(request):
    return render(request, 'about.html')
