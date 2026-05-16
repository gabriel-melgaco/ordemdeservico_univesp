from django.test import TestCase

from ordens.models import Empresa
from ordens.tests.factories import create_ordem


class OrdemDeServicoModelTests(TestCase):
    def test_default_status_and_string_representation(self):
        ordem = create_ordem(nome_guerra="Moura")

        self.assertEqual(ordem.status, "Aberta")
        self.assertEqual(str(ordem), f"OS #{ordem.id} - Moura (Aberta)")

    def test_default_purchase_status_is_pending(self):
        ordem = create_ordem()

        self.assertEqual(ordem.status_compra, "pendente")


class EmpresaModelTests(TestCase):
    def test_string_representation_uses_nome_fantasia(self):
        empresa = Empresa.objects.create(nome_fantasia="Fornecedor XPTO", cnpj="11.111.111/0001-11")

        self.assertEqual(str(empresa), "Fornecedor XPTO")

    def test_empresas_are_ordered_by_nome_fantasia(self):
        Empresa.objects.create(nome_fantasia="Zeta", cnpj="22.222.222/0001-22")
        Empresa.objects.create(nome_fantasia="Alpha", cnpj="33.333.333/0001-33")

        self.assertEqual(list(Empresa.objects.values_list("nome_fantasia", flat=True)), ["Alpha", "Zeta"])
