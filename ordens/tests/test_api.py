from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ordens.models import OrdemDeServico
from ordens.tests.factories import create_ordem, create_user_in_group, ordem_payload


@override_settings(ALLOWED_HOSTS=["testserver"])
class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def authenticate_as(self, group_name):
        user = create_user_in_group(username=f"user_{group_name}", group_name=group_name)
        self.client.force_authenticate(user=user)
        return user

    def test_token_endpoint_returns_user_token_and_groups(self):
        user = create_user_in_group(username="admin", group_name="Administrador", password="abc12345XYZ")

        response = self.client.post(
            "/api/auth/token/",
            {"username": "admin", "password": "abc12345XYZ"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], user.username)
        self.assertEqual(response.data["token"], Token.objects.get(user=user).key)
        self.assertEqual(response.data["grupos"], ["Administrador"])

    def test_ordens_list_requires_expected_group(self):
        create_ordem()
        self.authenticate_as("Compras")

        response = self.client.get("/api/ordens/")

        self.assertEqual(response.status_code, 403)

    def test_usuario_can_create_and_filter_ordens(self):
        self.authenticate_as("Usuario")

        response = self.client.post("/api/ordens/", ordem_payload(tipo_servico="computador"), format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(OrdemDeServico.objects.count(), 1)

        list_response = self.client.get("/api/ordens/", {"tipo_servico": "computador"})
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data["count"], 1)
        self.assertEqual(list_response.data["results"][0]["tipo_servico"], "computador")

    def test_tecnico_can_execute_ordem(self):
        ordem = create_ordem()
        self.authenticate_as("Tecnico")

        response = self.client.patch(
            f"/api/ordens/{ordem.pk}/executar/",
            {"nome_executante": "Tecnico", "prioridade_execucao": "alta"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        ordem.refresh_from_db()
        self.assertEqual(ordem.status, "Execu\u00e7\u00e3o")
        self.assertEqual(ordem.nome_executante, "Tecnico")

    def test_compras_endpoint_lists_only_pending_material_orders(self):
        pending = create_ordem(possui_material=False, material_necessario="Fonte")
        create_ordem(possui_material=True, material_necessario="Mouse")
        create_ordem(possui_material=False, material_necessario="")
        self.authenticate_as("Compras")

        response = self.client.get("/api/compras/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["status_compra"], pending.status_compra)
