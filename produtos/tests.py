from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Produto


class CadastroProdutoTestCase(TestCase):
    """Garante que o produto cadastrado apareça na listagem."""

    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Bebidas")

    def test_produto_cadastrado_aparece_na_listagem(self):
        resposta = self.client.post(
            reverse("adicionar_produto"),
            {
                "nome": "Refrigerante",
                "descricao": "Coca 2L",
                "preco": "5.00",
                "estoque": "10",
                "categoria": str(self.categoria.id),
            },
        )

        self.assertRedirects(resposta, reverse("produtos"))
        self.assertTrue(Produto.objects.filter(nome="Refrigerante").exists())

        listagem = self.client.get(reverse("produtos"))

        self.assertContains(listagem, "Refrigerante")
        self.assertContains(listagem, "Bebidas")

    def test_produto_pode_ser_cadastrado_sem_categoria(self):
        resposta = self.client.post(
            reverse("adicionar_produto"),
            {
                "nome": "Refrigerante",
                "descricao": "Coca 2L",
                "preco": "5.00",
                "estoque": "10",
                "categoria": "",
            },
        )

        self.assertRedirects(resposta, reverse("produtos"))

        produto = Produto.objects.get(nome="Refrigerante")

        self.assertIsNone(produto.categoria)
        self.assertContains(self.client.get(reverse("produtos")), "Sem categoria")

    def test_categoria_invalida_nao_cadastra_produto(self):
        resposta = self.client.post(
            reverse("adicionar_produto"),
            {
                "nome": "Refrigerante",
                "descricao": "",
                "preco": "5.00",
                "estoque": "10",
                "categoria": "9999",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Produto.objects.exists())
        self.assertContains(resposta, "Categoria inválida")

    def test_dados_invalidos_nao_cadastra_produto(self):
        resposta = self.client.post(
            reverse("adicionar_produto"),
            {
                "nome": "",
                "descricao": "",
                "preco": "abc",
                "estoque": "x",
                "categoria": "",
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Produto.objects.exists())
        self.assertContains(resposta, "Informe o nome do produto.")

    def test_preco_aceita_virgula_decimal(self):
        self.client.post(
            reverse("adicionar_produto"),
            {
                "nome": "Suco",
                "descricao": "",
                "preco": "4,50",
                "estoque": "8",
                "categoria": "",
            },
        )

        self.assertEqual(Produto.objects.get(nome="Suco").preco, Decimal("4.50"))


class EdicaoProdutoTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Bebidas")
        self.outra_categoria = Categoria.objects.create(nome="Salgados")
        self.produto = Produto.objects.create(
            nome="Suco",
            descricao="Laranja",
            preco=Decimal("4.50"),
            estoque=8,
            categoria=self.categoria,
        )

    def test_formulario_de_edicao_marca_categoria_atual(self):
        resposta = self.client.get(
            reverse("editar_produto", args=[self.produto.id])
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "selected")

    def test_edicao_preserva_dados(self):
        resposta = self.client.post(
            reverse("editar_produto", args=[self.produto.id]),
            {
                "nome": "Suco de Laranja",
                "descricao": "Laranja",
                "preco": "5.00",
                "estoque": "7",
                "categoria": str(self.outra_categoria.id),
            },
        )

        self.assertRedirects(resposta, reverse("produtos"))

        self.produto.refresh_from_db()

        self.assertEqual(self.produto.nome, "Suco de Laranja")
        self.assertEqual(self.produto.preco, Decimal("5.00"))
        self.assertEqual(self.produto.estoque, 7)
        self.assertEqual(self.produto.categoria, self.outra_categoria)


class CategoriasTestCase(TestCase):
    def test_pagina_de_categorias_carrega(self):
        resposta = self.client.get(reverse("categorias"))

        self.assertEqual(resposta.status_code, 200)

    def test_cadastro_de_categoria(self):
        resposta = self.client.post(
            reverse("adicionar_categoria"),
            {"nome": "Salgados", "descricao": "Lanches"},
        )

        self.assertRedirects(resposta, reverse("categorias"))
        self.assertTrue(Categoria.objects.filter(nome="Salgados").exists())
