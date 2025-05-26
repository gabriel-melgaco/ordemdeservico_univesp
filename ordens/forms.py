from django import forms
from .models import OrdemDeServico
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit


class OrdemDeServicoForm(forms.ModelForm):

    class Meta:
        model = OrdemDeServico
        fields = ['nome_guerra', 'posto', 'graduacao', 'telefone_contato', 'esquadrilha', 'funcao', 'tipo_servico', 'descricao_problema']
   
    def __init__(self, *args, **kwargs):
        super(OrdemDeServicoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('nome_guerra',
                      placeholder='Nome de Guerra',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('posto',
                      placeholder='Posto',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('graduacao',
                      placeholder='Graduação',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('telefone_contato',
                      placeholder='Telefone de Contato',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('esquadrilha',
                      placeholder='Qual sua Esquadrilha?',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('funcao',
                      placeholder='Qual sua Função?',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('tipo_servico',
                      placeholder='Qual sua Função?',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('descricao_problema',
                      placeholder='Descreva o problema apresentado',
                      css_class='form-control py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Submit('submit', 'Salvar',
                       css_class='btn bg-gradient-dark w-100 my-4 mb-2'),
                css_class="text-center"
            )
        )
 

class ExecutarOrdemForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['nome_executante', 'prioridade_execucao', 'possui_material', 'material_necessario', 'data_execucao']

class FinalizarOrdemForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['material_utilizado', 'ferramenta_utilizada', 'descricao_detalhada', 'numero_configuracao', 'modificacao_sistema']



class AtualizarStatusCompraForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['fornecedor', 'valor_compra', 'status_compra']
    
    def __init__(self, *args, **kwargs):
        super(AtualizarStatusCompraForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'text-start'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('fornecedor',
                      placeholder='Fornecedor',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('valor_compra',
                      placeholder='Valor da Compra',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Field('status_compra',
                      placeholder='Status da Compra',
                      css_class='form-control rounded-pill py-2 px-3 mb-3 shadow-sm border border-secondary'
                ),
            ),
            Div(
                Submit('submit', 'Salvar',
                       css_class='btn bg-gradient-dark w-100 my-4 mb-2'),
                css_class="text-center"
            )
        )
 
