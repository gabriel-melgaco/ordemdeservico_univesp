from rest_framework import serializers
from .models import OrdemDeServico, Empresa


class OrdemDeServicoListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listagens."""
    tipo_servico_display = serializers.CharField(source='get_tipo_servico_display', read_only=True)
    prioridade_display   = serializers.CharField(source='get_prioridade_execucao_display', read_only=True)
    status_compra_display = serializers.CharField(source='get_status_compra_display', read_only=True)

    class Meta:
        model = OrdemDeServico
        fields = [
            'id', 'nome_guerra', 'posto', 'esquadrilha', 'tipo_servico',
            'tipo_servico_display', 'status', 'data_criacao',
            'prioridade_execucao', 'prioridade_display',
            'status_compra', 'status_compra_display',
        ]
        read_only_fields = ['id', 'data_criacao', 'status']


class OrdemDeServicoDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para criação e detalhamento."""
    tipo_servico_display  = serializers.CharField(source='get_tipo_servico_display', read_only=True)
    prioridade_display    = serializers.CharField(source='get_prioridade_execucao_display', read_only=True)
    status_compra_display = serializers.CharField(source='get_status_compra_display', read_only=True)

    class Meta:
        model = OrdemDeServico
        fields = '__all__'
        read_only_fields = ['id', 'data_criacao', 'status']


class ExecutarOrdemSerializer(serializers.ModelSerializer):
    """Serializer para a etapa de execução."""

    class Meta:
        model = OrdemDeServico
        fields = ['nome_executante', 'prioridade_execucao', 'possui_material',
                  'material_necessario', 'data_execucao']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.status = 'Execução'
        instance.save()
        return instance


class FinalizarOrdemSerializer(serializers.ModelSerializer):
    """Serializer para a etapa de finalização."""

    class Meta:
        model = OrdemDeServico
        fields = ['material_utilizado', 'ferramenta_utilizada', 'descricao_detalhada',
                  'numero_configuracao', 'modificacao_sistema']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.status = 'Finalizada'
        instance.save()
        return instance


class AtualizarCompraSerializer(serializers.ModelSerializer):
    """Serializer para atualização de status de compra."""

    class Meta:
        model = OrdemDeServico
        fields = ['fornecedor', 'valor_compra', 'status_compra']


class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
