# Generated by Django 5.1.7 on 2025-03-25 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdemDeServico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_guerra', models.CharField(max_length=100)),
                ('posto', models.CharField(max_length=50)),
                ('graduacao', models.CharField(max_length=50)),
                ('telefone_contato', models.CharField(max_length=15)),
                ('esquadrilha', models.CharField(max_length=100)),
                ('funcao', models.CharField(max_length=100)),
                ('tipo_servico', models.CharField(choices=[('notebook', 'Manutenção de Notebook'), ('computador', 'Manutenção de Microcomputador'), ('acesso', 'Controle de Acesso')], max_length=50)),
                ('descricao_problema', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Aberta', editable=False, max_length=20)),
            ],
        ),
    ]
