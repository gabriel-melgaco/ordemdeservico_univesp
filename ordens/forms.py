from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import OrdemDeServico, Empresa
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit


FIELD_CSS = 'form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
TEXTAREA_CSS = 'form-control py-2 px-3 mb-3 shadow-sm border border-secondary'
SUBMIT_CSS = 'btn bg-gradient-dark w-100 my-4 mb-2'


class OrdemDeServicoForm(forms.ModelForm):

    class Meta:
        model = OrdemDeServico
        fields = ['nome_guerra', 'posto', 'graduacao', 'telefone_contato', 'esquadrilha', 'funcao', 'tipo_servico', 'descricao_problema']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Div(Field('nome_guerra', placeholder='Nome de Guerra', css_class=FIELD_CSS)),
            Div(Field('posto', placeholder='Posto', css_class=FIELD_CSS)),
            Div(Field('graduacao', placeholder='Graduação', css_class=FIELD_CSS)),
            Div(Field('telefone_contato', placeholder='Telefone de Contato', css_class=FIELD_CSS)),
            Div(Field('esquadrilha', placeholder='Qual sua Esquadrilha?', css_class=FIELD_CSS)),
            Div(Field('funcao', placeholder='Qual sua Função?', css_class=FIELD_CSS)),
            Div(Field('tipo_servico', css_class=FIELD_CSS)),
            Div(Field('descricao_problema', placeholder='Descreva o problema apresentado', css_class=TEXTAREA_CSS)),
            Div(Submit('submit', 'Salvar', css_class=SUBMIT_CSS), css_class="text-center"),
        )


class ExecutarOrdemForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['nome_executante', 'prioridade_execucao', 'possui_material', 'material_necessario', 'data_execucao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Div(Field('nome_executante', placeholder='Nome do Executante', css_class=FIELD_CSS)),
            Div(Field('prioridade_execucao', css_class=FIELD_CSS)),
            Div(Field('possui_material', css_class='form-check-input')),
            Div(Field('material_necessario', placeholder='Descreva o material necessário', css_class=TEXTAREA_CSS)),
            Div(Field('data_execucao', css_class=FIELD_CSS)),
            Div(Submit('submit', 'Salvar', css_class=SUBMIT_CSS), css_class="text-center"),
        )


class FinalizarOrdemForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['material_utilizado', 'ferramenta_utilizada', 'descricao_detalhada', 'numero_configuracao', 'modificacao_sistema']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Div(Field('material_utilizado', placeholder='Material utilizado', css_class=TEXTAREA_CSS)),
            Div(Field('ferramenta_utilizada', placeholder='Ferramenta utilizada', css_class=TEXTAREA_CSS)),
            Div(Field('descricao_detalhada', placeholder='Descrição detalhada do serviço', css_class=TEXTAREA_CSS)),
            Div(Field('numero_configuracao', placeholder='Número de configuração (se aplicável)', css_class=FIELD_CSS)),
            Div(Field('modificacao_sistema', placeholder='Descreva modificações no sistema', css_class=TEXTAREA_CSS)),
            Div(Submit('submit', 'Finalizar', css_class=SUBMIT_CSS), css_class="text-center"),
        )


class AtualizarStatusCompraForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['fornecedor', 'valor_compra', 'status_compra']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Div(Field('fornecedor', placeholder='Fornecedor', css_class=FIELD_CSS)),
            Div(Field('valor_compra', placeholder='Valor da Compra', css_class=FIELD_CSS)),
            Div(Field('status_compra', css_class=FIELD_CSS)),
            Div(Submit('submit', 'Salvar', css_class=SUBMIT_CSS), css_class="text-center"),
        )


class CriarEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_fantasia', 'razao_social', 'cnpj', 'inscricao_estadual',
            'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep',
            'telefone', 'email', 'contato_responsavel', 'site',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Div(Field('nome_fantasia', placeholder='Nome Fantasia', css_class=FIELD_CSS)),
            Div(Field('razao_social', placeholder='Razão Social', css_class=FIELD_CSS)),
            Div(Field('cnpj', placeholder='00.000.000/0000-00', css_class=FIELD_CSS)),
            Div(Field('inscricao_estadual', placeholder='Inscrição Estadual', css_class=FIELD_CSS)),
            Div(Field('endereco', placeholder='Endereço', css_class=FIELD_CSS)),
            Div(Field('numero', placeholder='Número', css_class=FIELD_CSS)),
            Div(Field('complemento', placeholder='Complemento', css_class=FIELD_CSS)),
            Div(Field('bairro', placeholder='Bairro', css_class=FIELD_CSS)),
            Div(Field('cidade', placeholder='Cidade', css_class=FIELD_CSS)),
            Div(Field('estado', placeholder='UF', css_class=FIELD_CSS)),
            Div(Field('cep', placeholder='00000-000', css_class=FIELD_CSS)),
            Div(Field('telefone', placeholder='Telefone', css_class=FIELD_CSS)),
            Div(Field('email', placeholder='E-mail', css_class=FIELD_CSS)),
            Div(Field('contato_responsavel', placeholder='Contato Responsável', css_class=FIELD_CSS)),
            Div(Field('site', placeholder='https://...', css_class=FIELD_CSS)),
            Div(Submit('submit', 'Salvar Empresa', css_class=SUBMIT_CSS), css_class="text-center"),
        )


class RegistrarUsuarioForm(UserCreationForm):
    """
    Estende UserCreationForm para permitir a seleção de grupo
    durante o cadastro de usuário pelo Administrador.
    """
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Grupo de Acesso",
        help_text="Selecione o grupo que define as permissões do usuário no sistema.",
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'grupo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Div(Field('username', css_class=FIELD_CSS)),
            Div(Field('first_name', placeholder='Nome', css_class=FIELD_CSS)),
            Div(Field('last_name', placeholder='Sobrenome', css_class=FIELD_CSS)),
            Div(Field('email', placeholder='E-mail', css_class=FIELD_CSS)),
            Div(Field('password1', css_class=FIELD_CSS)),
            Div(Field('password2', css_class=FIELD_CSS)),
            Div(Field('grupo', css_class=FIELD_CSS)),
            Div(Submit('submit', 'Cadastrar Usuário', css_class=SUBMIT_CSS), css_class="text-center"),
        )
