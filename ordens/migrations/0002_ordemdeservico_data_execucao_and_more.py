# Generated by Django 5.1.7 on 2025-03-25 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordens', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemdeservico',
            name='data_execucao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='descricao_detalhada',
            field=models.TextField(blank=True, null=True, verbose_name='Descrição Detalhada'),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='ferramenta_utilizada',
            field=models.TextField(blank=True, null=True, verbose_name='Ferramenta Utilizada'),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='material_necessario',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='material_utilizado',
            field=models.TextField(blank=True, null=True, verbose_name='Material Utilizado'),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='modificacao_sistema',
            field=models.TextField(blank=True, null=True, verbose_name='Modificação no Sistema (se aplicável)'),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='nome_executante',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='numero_configuracao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número de Configuração'),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='possui_material',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='prioridade_execucao',
            field=models.CharField(blank=True, choices=[('alta', 'Alta'), ('media', 'Média'), ('baixa', 'Baixa')], max_length=20, null=True),
        ),
    ]
