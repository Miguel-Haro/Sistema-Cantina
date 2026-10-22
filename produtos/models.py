from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        related_name="produtos",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name="vendas"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="vendas"
    )

    quantidade = models.PositiveIntegerField()

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.pessoa.nome} - {self.produto.nome}"


class ContaReceber(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("pago", "Pago"),
    ]

    venda = models.OneToOneField(
        Venda,
        on_delete=models.CASCADE,
        related_name="conta_receber"
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    vencimento = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pendente"
    )

    data_pagamento = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Conta #{self.id} - {self.venda.pessoa.nome}"