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

class Empresa(models.Model):
    nome_fantasia = models.CharField("Nome Fantasia", max_length=150)
    razao_social = models.CharField("Razão Social", max_length=150, null=True, blank=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)  # formato sugerido: 00.000.000/0000-00
    inscricao_estadual = models.CharField("Inscrição Estadual", max_length=50, null=True, blank=True)

    endereco = models.CharField("Endereço", max_length=255, null=True, blank=True)
    numero = models.CharField("Número", max_length=20, null=True, blank=True)
    complemento = models.CharField("Complemento", max_length=100, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=100, null=True, blank=True)
    cidade = models.CharField("Cidade", max_length=100, null=True, blank=True)
    estado = models.CharField("Estado", max_length=2, null=True, blank=True)
    cep = models.CharField("CEP", max_length=9, null=True, blank=True)

    telefone = models.CharField("Telefone", max_length=20, null=True, blank=True)
    email = models.EmailField("E-mail", null=True, blank=True)
    contato_responsavel = models.CharField("Contato Responsável", max_length=100, null=True, blank=True)
    site = models.URLField("Site", null=True, blank=True)

    ativo = models.BooleanField("Ativo", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["nome_fantasia"]

    def __str__(self):
        return self.nome_fantasia
    