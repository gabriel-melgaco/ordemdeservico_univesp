from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import OrdemDeServico, Empresa


# ─── Inline de grupos no admin de usuários ───────────────────────────────────

class UserGroupInline(admin.TabularInline):
    model = User.groups.through
    extra = 1
    verbose_name = "Grupo"
    verbose_name_plural = "Grupos do Usuário"


# ─── Admin de Usuário customizado ────────────────────────────────────────────

class CustomUserAdmin(BaseUserAdmin):
    """
    Substitui o UserAdmin padrão para expor gerenciamento de grupos
    e permissões diretamente na tela do usuário.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'get_grupos')
    list_filter = ('is_active', 'is_staff', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Campos exibidos no formulário de edição
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': (
                'Atribua o usuário aos grupos: <strong>Administrador</strong>, '
                '<strong>Usuario</strong>, <strong>Tecnico</strong> ou <strong>Compras</strong>. '
                'Os grupos controlam o acesso a cada módulo do sistema.'
            ),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # filter_horizontal torna a seleção de grupos e permissões mais amigável
    filter_horizontal = ('groups', 'user_permissions')

    @admin.display(description='Grupos')
    def get_grupos(self, obj):
        return ", ".join([g.name for g in obj.groups.all()]) or "—"


# Re-registra o User com o admin customizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ─── Admin de Grupos ──────────────────────────────────────────────────────────

class CustomGroupAdmin(admin.ModelAdmin):
    """
    Exibe os membros de cada grupo e facilita a criação dos grupos padrão
    do sistema (Administrador, Usuario, Tecnico, Compras).
    """
    list_display = ('name', 'get_membros')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)

    @admin.display(description='Membros')
    def get_membros(self, obj):
        membros = obj.user_set.all()
        if membros:
            return ", ".join([u.username for u in membros])
        return "Nenhum membro"


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)


# ─── Admin de Ordem de Serviço ────────────────────────────────────────────────

@admin.register(OrdemDeServico)
class OrdemDeServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_guerra', 'posto', 'tipo_servico', 'status', 'data_criacao', 'prioridade_execucao')
    list_filter = ('status', 'tipo_servico', 'prioridade_execucao', 'status_compra')
    search_fields = ('nome_guerra', 'posto', 'esquadrilha', 'descricao_problema')
    readonly_fields = ('data_criacao',)
    date_hierarchy = 'data_criacao'
    ordering = ('-data_criacao',)

    fieldsets = (
        ('Dados do Solicitante', {
            'fields': ('nome_guerra', 'posto', 'graduacao', 'telefone_contato', 'esquadrilha', 'funcao')
        }),
        ('Serviço', {
            'fields': ('tipo_servico', 'descricao_problema', 'status', 'data_criacao')
        }),
        ('Execução', {
            'fields': ('nome_executante', 'prioridade_execucao', 'possui_material', 'material_necessario', 'data_execucao'),
            'classes': ('collapse',),
        }),
        ('Finalização', {
            'fields': ('material_utilizado', 'ferramenta_utilizada', 'descricao_detalhada', 'numero_configuracao', 'modificacao_sistema'),
            'classes': ('collapse',),
        }),
        ('Compras', {
            'fields': ('fornecedor', 'valor_compra', 'status_compra'),
            'classes': ('collapse',),
        }),
    )

    # Permite editar status (sobrescreve editable=False apenas no admin)
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        # status permanece editável no admin para correções manuais
        return readonly


# ─── Admin de Empresa ─────────────────────────────────────────────────────────

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj', 'cidade', 'estado', 'telefone', 'ativo')
    list_filter = ('ativo', 'estado')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')
    readonly_fields = ('criado_em', 'atualizado_em')

    fieldsets = (
        ('Identificação', {
            'fields': ('nome_fantasia', 'razao_social', 'cnpj', 'inscricao_estadual', 'ativo')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'contato_responsavel', 'site')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',),
        }),
    )


# ─── Personalização do site admin ────────────────────────────────────────────

admin.site.site_header = "SisGeOS — Administração"
admin.site.site_title = "SisGeOS Admin"
admin.site.index_title = "Painel de Administração"
