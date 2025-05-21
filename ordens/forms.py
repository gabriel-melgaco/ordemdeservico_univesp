from django import forms
from .models import OrdemDeServico

class OrdemDeServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['nome_guerra', 'posto', 'graduacao', 'telefone_contato', 'esquadrilha', 'funcao', 'tipo_servico', 'descricao_problema']

class ExecutarOrdemForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['nome_executante', 'prioridade_execucao', 'possui_material', 'material_necessario', 'data_execucao']

class FinalizarOrdemForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['material_utilizado', 'ferramenta_utilizada', 'descricao_detalhada', 'numero_configuracao', 'modificacao_sistema']

from django import forms
from .models import OrdemDeServico

class AtualizarStatusCompraForm(forms.ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['fornecedor', 'valor_compra', 'status_compra']
        widgets = {
            'fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'status_compra': forms.Select(attrs={'class': 'form-control'}),
        }
