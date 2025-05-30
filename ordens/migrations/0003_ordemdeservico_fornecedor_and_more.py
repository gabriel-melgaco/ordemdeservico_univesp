# Generated by Django 5.1.7 on 2025-03-29 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordens', '0002_ordemdeservico_data_execucao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemdeservico',
            name='fornecedor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='status_compra',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('negociado', 'Negociado'), ('entregue', 'Entregue'), ('disponivel', 'Disponível'), ('deferido', 'Deferido')], default='pendente', max_length=20),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='valor_compra',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
