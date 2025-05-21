from django.db import models

# Create your models here.

class OrdemDeServico(models.Model):
    TIPO_SERVICO_CHOICES = [
        ('notebook', 'Manutenção de Notebook'),
        ('computador', 'Manutenção de Microcomputador'),
        ('acesso', 'Controle de Acesso'),
    ]
    nome_guerra = models.CharField(max_length=100)
    posto = models.CharField(max_length=50)
    graduacao = models.CharField(max_length=50)
    telefone_contato = models.CharField(max_length=15)
    esquadrilha = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100)
    tipo_servico = models.CharField(max_length=50, choices=TIPO_SERVICO_CHOICES)
    descricao_problema = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Aberta', editable=False)

    # Campos para a execução da ordem
    nome_executante = models.CharField(max_length=100, null=True, blank=True)
    prioridade_execucao = models.CharField(max_length=20, choices=[('alta', 'Alta'), ('media', 'Média'), ('baixa', 'Baixa')], null=True, blank=True)
    possui_material = models.BooleanField(default=False)
    material_necessario = models.TextField(null=True, blank=True)
    data_execucao = models.DateTimeField(null=True, blank=True)

    # Campos para a finalização da ordem
    material_utilizado = models.TextField(null=True, blank=True, verbose_name="Material Utilizado")
    ferramenta_utilizada = models.TextField(null=True, blank=True, verbose_name="Ferramenta Utilizada")
    descricao_detalhada = models.TextField(null=True, blank=True, verbose_name="Descrição Detalhada")
    numero_configuracao = models.CharField(max_length=100, null=True, blank=True, verbose_name="Número de Configuração")
    modificacao_sistema = models.TextField(null=True, blank=True, verbose_name="Modificação no Sistema (se aplicável)")

    # Campos para Compras
    fornecedor = models.CharField(max_length=100, null=True, blank=True)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status_compra = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('negociado', 'Negociado'),
            ('entregue', 'Entregue'),
            ('disponivel', 'Disponível'),
            ('deferido', 'Deferido')
        ],
        default='pendente'
    )