from django.test import TestCase

from ordens.forms import CriarEmpresaForm, OrdemDeServicoForm
from ordens.models import Empresa
from ordens.tests.factories import ordem_payload


class FormTests(TestCase):
    def test_ordem_de_servico_form_accepts_required_fields(self):
        form = OrdemDeServicoForm(data=ordem_payload())

        self.assertTrue(form.is_valid(), form.errors)
        ordem = form.save()

        self.assertEqual(ordem.status, "Aberta")
        self.assertEqual(ordem.tipo_servico, "notebook")

    def test_criar_empresa_form_rejects_duplicate_cnpj(self):
        Empresa.objects.create(nome_fantasia="Empresa A", cnpj="00.000.000/0001-00")

        form = CriarEmpresaForm(data={
            "nome_fantasia": "Empresa B",
            "cnpj": "00.000.000/0001-00",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("cnpj", form.errors)
