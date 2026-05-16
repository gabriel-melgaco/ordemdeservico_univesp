from django.contrib.auth.models import Group, User

from ordens.models import OrdemDeServico


def create_user_in_group(username="usuario", group_name="Usuario", password="senha-forte-123"):
    group, _ = Group.objects.get_or_create(name=group_name)
    user = User.objects.create_user(username=username, password=password)
    user.groups.add(group)
    return user


def ordem_payload(**overrides):
    payload = {
        "nome_guerra": "Silva",
        "posto": "1 Ten",
        "graduacao": "Tenente",
        "telefone_contato": "11999999999",
        "esquadrilha": "Alpha",
        "funcao": "Analista",
        "tipo_servico": "notebook",
        "descricao_problema": "Equipamento nao liga.",
    }
    payload.update(overrides)
    return payload


def create_ordem(**overrides):
    return OrdemDeServico.objects.create(**ordem_payload(**overrides))
