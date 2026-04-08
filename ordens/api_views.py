"""
Views da API REST do SisGeOS.

Autenticação: Token (Authorization: Token <token>) ou Sessão Django.
Autorização:  baseada nos grupos do sistema (Administrador, Usuario, Tecnico, Compras).
"""
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import authenticate

from .models import OrdemDeServico, Empresa
from .serializers import (
    OrdemDeServicoListSerializer,
    OrdemDeServicoDetailSerializer,
    ExecutarOrdemSerializer,
    FinalizarOrdemSerializer,
    AtualizarCompraSerializer,
    EmpresaSerializer,
)


# ─── Permissões por grupo ─────────────────────────────────────────────────────

class IsAdminOrUsuarioOrTecnico(BasePermission):
    """Permite acesso aos grupos Administrador, Usuario e Tecnico."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name__in=['Administrador', 'Usuario', 'Tecnico']).exists()
        )


class IsAdminOrTecnico(BasePermission):
    """Permite acesso aos grupos Administrador e Tecnico."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name__in=['Administrador', 'Tecnico']).exists()
        )


class IsAdminOrCompras(BasePermission):
    """Permite acesso aos grupos Administrador e Compras."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name__in=['Administrador', 'Compras']).exists()
        )


class IsAdministrador(BasePermission):
    """Permite acesso apenas ao grupo Administrador."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Administrador').exists()
        )


# ─── Autenticação ─────────────────────────────────────────────────────────────

@extend_schema(tags=['auth'])
class ObterTokenView(APIView):
    """
    Autentica o usuário com username + password e retorna o Token de acesso.

    Use o token retornado no header:
    `Authorization: Token <token>`
    """
    permission_classes = []

    @extend_schema(
        summary='Obter token de acesso',
        request=AuthTokenSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string', 'example': 'abc123...'},
                    'user_id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'grupos': {'type': 'array', 'items': {'type': 'string'}},
                },
            },
            400: {'description': 'Credenciais inválidas'},
        },
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Informe username e password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {'error': 'Credenciais inválidas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        grupos = list(user.groups.values_list('name', flat=True))
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'grupos': grupos,
        })


# ─── Ordens de Serviço ────────────────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        summary='Listar todas as ordens de serviço',
        tags=['ordens'],
        parameters=[
            OpenApiParameter('status', OpenApiTypes.STR,
                             description='Filtrar por status (Aberta, Execução, Finalizada)'),
            OpenApiParameter('tipo_servico', OpenApiTypes.STR,
                             description='Filtrar por tipo (notebook, computador, acesso)'),
        ],
    ),
    create=extend_schema(summary='Criar nova ordem de serviço', tags=['ordens']),
    retrieve=extend_schema(summary='Detalhar ordem de serviço', tags=['ordens']),
    partial_update=extend_schema(summary='Atualizar campos da ordem', tags=['ordens']),
    destroy=extend_schema(summary='Excluir ordem de serviço (somente Administrador)', tags=['ordens']),
)
class OrdemDeServicoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    CRUD de Ordens de Serviço.

    - **Listar / Detalhar / Criar**: Administrador, Usuario, Tecnico
    - **Executar / Finalizar**: Administrador, Tecnico
    - **Excluir**: somente Administrador
    """
    queryset = OrdemDeServico.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'list':
            return OrdemDeServicoListSerializer
        if self.action == 'executar':
            return ExecutarOrdemSerializer
        if self.action == 'finalizar':
            return FinalizarOrdemSerializer
        return OrdemDeServicoDetailSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdministrador()]
        if self.action in ('executar', 'finalizar'):
            return [IsAdminOrTecnico()]
        return [IsAdminOrUsuarioOrTecnico()]

    def get_queryset(self):
        qs = OrdemDeServico.objects.all()
        status_param = self.request.query_params.get('status')
        tipo_param   = self.request.query_params.get('tipo_servico')
        if status_param:
            qs = qs.filter(status=status_param)
        if tipo_param:
            qs = qs.filter(tipo_servico=tipo_param)
        return qs

    @extend_schema(
        summary='Registrar execução da ordem',
        tags=['ordens'],
        request=ExecutarOrdemSerializer,
        responses={200: OrdemDeServicoDetailSerializer},
    )
    @action(detail=True, methods=['patch'], url_path='executar')
    def executar(self, request, pk=None):
        """Atualiza dados de execução e muda o status para **Execução**."""
        ordem = self.get_object()
        serializer = ExecutarOrdemSerializer(ordem, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        ordem = serializer.save()
        return Response(OrdemDeServicoDetailSerializer(ordem).data)

    @extend_schema(
        summary='Registrar finalização da ordem',
        tags=['ordens'],
        request=FinalizarOrdemSerializer,
        responses={200: OrdemDeServicoDetailSerializer},
    )
    @action(detail=True, methods=['patch'], url_path='finalizar')
    def finalizar(self, request, pk=None):
        """Atualiza dados de finalização e muda o status para **Finalizada**."""
        ordem = self.get_object()
        serializer = FinalizarOrdemSerializer(ordem, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        ordem = serializer.save()
        return Response(OrdemDeServicoDetailSerializer(ordem).data)


# ─── Compras ──────────────────────────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        summary='Listar ordens com material pendente de compra',
        tags=['ordens'],
    ),
    partial_update=extend_schema(
        summary='Atualizar fornecedor e status de compra',
        tags=['ordens'],
    ),
)
class ComprasViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Ordens que possuem `possui_material=False` e `material_necessario` preenchido.
    Acessível por **Administrador** e **Compras**.
    """
    serializer_class = AtualizarCompraSerializer
    permission_classes = [IsAdminOrCompras]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return OrdemDeServico.objects.filter(
            possui_material=False,
            material_necessario__isnull=False,
        ).exclude(material_necessario='')


# ─── Empresas ─────────────────────────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(summary='Listar empresas', tags=['empresas']),
    create=extend_schema(summary='Cadastrar empresa', tags=['empresas']),
    retrieve=extend_schema(summary='Detalhar empresa', tags=['empresas']),
    partial_update=extend_schema(summary='Atualizar empresa', tags=['empresas']),
    destroy=extend_schema(summary='Excluir empresa (somente Administrador)', tags=['empresas']),
)
class EmpresaViewSet(viewsets.ModelViewSet):
    """
    CRUD de Empresas / Fornecedores.
    Acessível por **Administrador** e **Compras**; exclusão apenas por **Administrador**.
    """
    serializer_class = EmpresaSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        qs = Empresa.objects.all()
        ativo = self.request.query_params.get('ativo')
        if ativo is not None:
            qs = qs.filter(ativo=ativo.lower() == 'true')
        return qs

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdministrador()]
        return [IsAdminOrCompras()]
