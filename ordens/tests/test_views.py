from django.test import TestCase, override_settings
from django.urls import reverse

from ordens.models import OrdemDeServico
from ordens.tests.factories import create_ordem, create_user_in_group, ordem_payload


@override_settings(ALLOWED_HOSTS=["testserver"])
class WebViewTests(TestCase):
    def login_as(self, group_name):
        user = create_user_in_group(username=f"user_{group_name}", group_name=group_name)
        self.client.force_login(user)
        return user

    def test_protected_view_redirects_user_without_group_to_permission_error(self):
        user = create_user_in_group(username="sem_grupo", group_name="Outro")
        self.client.force_login(user)

        response = self.client.get(reverse("listar_ordens"))

        self.assertRedirects(response, reverse("erro_permissao"))

    def test_usuario_can_create_ordem(self):
        self.login_as("Usuario")

        response = self.client.post(reverse("criar_ordem"), data=ordem_payload())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrdemDeServico.objects.count(), 1)
        self.assertContains(response, "Ordem de servi\u00e7o criada com sucesso!")

    def test_tecnico_can_mark_ordem_as_in_execution(self):
        ordem = create_ordem()
        self.login_as("Tecnico")

        response = self.client.post(
            reverse("executar_ordem", args=[ordem.pk]),
            data={
                "nome_executante": "Tecnico",
                "prioridade_execucao": "media",
                "possui_material": "",
                "material_necessario": "Memoria RAM",
                "data_execucao": "2026-05-16 10:00:00",
            },
        )

        self.assertRedirects(response, reverse("listar_ordens"))
        ordem.refresh_from_db()
        self.assertEqual(ordem.status, "Execu\u00e7\u00e3o")
        self.assertEqual(ordem.material_necessario, "Memoria RAM")

    def test_listar_compras_filters_orders_with_missing_material(self):
        compra = create_ordem(nome_guerra="Compra", possui_material=False, material_necessario="Fonte")
        create_ordem(nome_guerra="Sem necessidade", possui_material=True, material_necessario="Mouse")
        create_ordem(nome_guerra="Sem descricao", possui_material=False, material_necessario="")
        self.login_as("Compras")

        response = self.client.get(reverse("listar_compras"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["compras"], [compra])

    def test_buscar_por_numero_reports_non_numeric_input(self):
        self.login_as("Usuario")

        response = self.client.get(reverse("buscar_por_numero"), {"numero_ordem": "abc"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["erro"], "O n\u00famero da ordem deve ser um valor num\u00e9rico.")
