from decimal import Decimal, InvalidOperation
from datetime import timedelta

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone

from .models import (
    Produto,
    Categoria,
    Pessoa,
    Venda,
    ContaReceber,
)



# =========================
# DASHBOARD
# =========================

def dashboard(request):
    hoje = timezone.localdate()
    inicio = hoje - timedelta(days=6)

    # Vendas realizadas hoje
    vendas = Venda.objects.filter(
        data__date=hoje
    ).count()

    valor_vendas_hoje = Venda.objects.filter(
        data__date=hoje
    ).aggregate(
        total=Sum("total")
    )["total"] or Decimal("0.00")

    #Estoque com produto baixo
    produtos_estoque_baixo = Produto.objects.filter(
    estoque__lte=5
   ).order_by("estoque", "nome")

    # Últimas 5 vendas cadastradas
    ultimas_vendas = Venda.objects.select_related(
        "pessoa",
        "produto",
    ).order_by("-data")[:5]

    # Dados do gráfico: últimos 7 dias, incluindo hoje
    grafico_vendas = []

    for i in range(7):
        dia = inicio + timedelta(days=i)

        total_dia = Venda.objects.filter(
            data__date=dia
        ).aggregate(
            total=Sum("total")
        )["total"] or Decimal("0.00")

        grafico_vendas.append({
            "dia": dia.strftime("%d/%m"),
            "total": float(total_dia),
        })

    return render(
        request,
        "dashboard.html",
        {
            "vendas": vendas,
            "valor_vendas_hoje": valor_vendas_hoje,
            "ultimas_vendas": ultimas_vendas,
            "grafico_vendas": grafico_vendas,
            "produtos_estoque_baixo": produtos_estoque_baixo,
        },
        
    )


# =========================
# PRODUTOS
# =========================

def _dados_produto(request):
    """Lê e valida os campos do formulário de produto.

    Retorna (dados, erro). Quando há erro, "dados" ainda contém o que
    foi digitado para o formulário ser reexibido sem perder informações.
    """

    nome = (request.POST.get("nome") or "").strip()
    descricao = (request.POST.get("descricao") or "").strip()
    preco = (request.POST.get("preco") or "").strip().replace(",", ".")
    estoque = (request.POST.get("estoque") or "").strip()
    categoria_id = (request.POST.get("categoria") or "").strip()

    dados = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "estoque": estoque,
        "categoria_id": categoria_id,
        "preco_valor": None,
        "estoque_valor": None,
        "categoria": None,
    }

    if not nome:
        return dados, "Informe o nome do produto."

    try:
        preco_valor = Decimal(preco)
        estoque_valor = int(estoque)
    except (InvalidOperation, ValueError):
        return dados, "Informe preço e estoque válidos."

    if preco_valor < 0 or estoque_valor < 0:
        return dados, "Preço e estoque não podem ser negativos."

    categoria = None

    if categoria_id:
        categoria = Categoria.objects.filter(id=categoria_id).first()

        if categoria is None:
            return dados, "Categoria inválida."

    dados["preco_valor"] = preco_valor
    dados["estoque_valor"] = estoque_valor
    dados["categoria"] = categoria

    return dados, None


def _dados_produto_atual(produto):
    """Dados do produto salvo, usados para preencher o formulário."""

    return {
        "nome": produto.nome,
        "descricao": produto.descricao,
        "preco": str(produto.preco),
        "estoque": str(produto.estoque),
        "categoria_id": produto.categoria_id,
    }


def produtos(request):
    lista_produtos = Produto.objects.select_related("categoria").all()

    return render(
        request,
        "produtos.html",
        {"produtos": lista_produtos},
    )

def cadastrar_produto(request):
    categorias = Categoria.objects.all()

    if request.method == "POST":
        dados, erro = _dados_produto(request)

        if erro:
            messages.error(request, erro)

            return render(
                request,
                "cadastrar_produto.html",
                {"categorias": categorias, "dados": dados}
            )

        try:
            Produto.objects.create(
                nome=dados["nome"],
                descricao=dados["descricao"],
                preco=dados["preco_valor"],
                estoque=dados["estoque_valor"],
                categoria=dados["categoria"],
            )
        except (InvalidOperation, ValidationError):
            messages.error(
                request,
                "Não foi possível cadastrar o produto. Verifique os valores informados.",
            )

            return render(
                request,
                "cadastrar_produto.html",
                {"categorias": categorias, "dados": dados}
            )

        messages.success(
            request,
            "Produto cadastrado com sucesso!"
        )

        return redirect("produtos")

    return render(
        request,
        "cadastrar_produto.html",
        {"categorias": categorias, "dados": {}}
    )


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    categorias = Categoria.objects.all()

    if request.method == "POST":
        dados, erro = _dados_produto(request)

        if erro:
            messages.error(request, erro)

            return render(
                request,
                "editar_produto.html",
                {
                    "produto": produto,
                    "categorias": categorias,
                    "dados": dados,
                },
            )

        produto.nome = dados["nome"]
        produto.descricao = dados["descricao"]
        produto.preco = dados["preco_valor"]
        produto.estoque = dados["estoque_valor"]
        produto.categoria = dados["categoria"]

        try:
            produto.save()
        except (InvalidOperation, ValidationError):
            messages.error(
                request,
                "Não foi possível salvar o produto. Verifique os valores informados.",
            )

            return render(
                request,
                "editar_produto.html",
                {
                    "produto": produto,
                    "categorias": categorias,
                    "dados": dados,
                },
            )

        messages.success(request, "Produto atualizado com sucesso!")
        return redirect("produtos")

    return render(
        request,
        "editar_produto.html",
        {
            "produto": produto,
            "categorias": categorias,
            "dados": _dados_produto_atual(produto),
        },
    )


def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == "POST":
        produto.delete()

        messages.success(
            request,
            "Produto excluído com sucesso!"
        )

        return redirect("produtos")

    return render(
        request,
        "excluir_produto.html",
        {"produto": produto},
    )

def produtos_estoque_baixo(request):
    limite_estoque = 5

    produtos = Produto.objects.filter(
        estoque__lte=limite_estoque
    ).order_by("estoque", "nome")

    return render(
        request,
        "estoque_baixo.html",
        {
            "produtos": produtos,
            "limite_estoque": limite_estoque,
        },
    )


# =========================
# CATEGORIAS
# =========================

def categorias(request):
    lista_categorias = Categoria.objects.all()

    return render(
        request,
        "categorias.html",
        {"categorias": lista_categorias},
    )


def adicionar_categoria(request):
    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip()
        descricao = (request.POST.get("descricao") or "").strip()

        if not nome:
            messages.error(request, "Informe o nome da categoria.")

            return render(request, "adicionar_categoria.html")

        Categoria.objects.create(
            nome=nome,
            descricao=descricao,
        )

        messages.success(request, "Categoria cadastrada com sucesso!")
        return redirect("categorias")

    return render(request, "adicionar_categoria.html")


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip()
        descricao = (request.POST.get("descricao") or "").strip()

        if not nome:
            messages.error(request, "Informe o nome da categoria.")

            return render(
                request,
                "editar_categoria.html",
                {"categoria": categoria},
            )

        categoria.nome = nome
        categoria.descricao = descricao
        categoria.save()

        messages.success(request, "Categoria atualizada com sucesso!")
        return redirect("categorias")

    return render(
        request,
        "editar_categoria.html",
        {"categoria": categoria},
    )


def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        categoria.delete()
        messages.success(request, "Categoria excluída com sucesso!")
        return redirect("categorias")

    return render(
        request,
        "excluir_categoria.html",
        {"categoria": categoria},
    )


# =========================
# PESSOAS
# =========================

def pessoas(request):
    lista_pessoas = Pessoa.objects.all()

    return render(
        request,
        "pessoas.html",
        {"pessoas": lista_pessoas},
    )


def cadastrar_pessoa(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")

        Pessoa.objects.create(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email,
        )

        messages.success(request, "Pessoa cadastrada com sucesso!")
        return redirect("pessoas")

    return render(request, "cadastrar_pessoa.html")


def editar_pessoa(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)

    if request.method == "POST":
        pessoa.nome = request.POST.get("nome")
        pessoa.cpf = request.POST.get("cpf")
        pessoa.telefone = request.POST.get("telefone")
        pessoa.email = request.POST.get("email")

        pessoa.save()

        messages.success(request, "Pessoa atualizada com sucesso!")
        return redirect("pessoas")

    return render(
        request,
        "editar_pessoa.html",
        {"pessoa": pessoa},
    )


def excluir_pessoa(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)

    if request.method == "POST":
        pessoa.delete()
        messages.success(request, "Pessoa excluída com sucesso!")
        return redirect("pessoas")

    return render(
        request,
        "excluir_pessoa.html",
        {"pessoa": pessoa},
    )


# =========================
# VENDAS
# =========================

def vendas(request):
    lista_vendas = Venda.objects.select_related(
        "pessoa",
        "produto",
    ).order_by("-data")

    return render(
        request,
        "vendas.html",
        {"vendas": lista_vendas},
    )


def cadastrar_venda(request):
    pessoas_lista = Pessoa.objects.all()
    produtos_lista = Produto.objects.filter(estoque__gt=0)

    if request.method == "POST":
        try:
            pessoa_id = request.POST.get("pessoa")
            produto_id = request.POST.get("produto")
            quantidade = int(request.POST.get("quantidade", "0"))
        except (TypeError, ValueError):
            messages.error(request, "Informe uma quantidade válida.")
            return redirect("cadastrar_venda")

        if quantidade <= 0:
            messages.error(
                request,
                "A quantidade deve ser maior que zero.",
            )
            return redirect("cadastrar_venda")

        pessoa = get_object_or_404(Pessoa, id=pessoa_id)
        produto = get_object_or_404(Produto, id=produto_id)

        if quantidade > produto.estoque:
            messages.error(
                request,
                f"Estoque insuficiente. Disponível: {produto.estoque}.",
            )
            return redirect("cadastrar_venda")

        preco_unitario = produto.preco
        total = preco_unitario * quantidade

        # Registra a venda
        venda = Venda.objects.create(
            pessoa=pessoa,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            total=total,
        )

        # Cria a conta a receber com vencimento em 30 dias
        ContaReceber.objects.create(
            venda=venda,
            valor=total,
            vencimento=timezone.localdate() + timedelta(days=30),
            status="pendente",
        )

        # Atualiza o estoque
        produto.estoque -= quantidade
        produto.save(update_fields=["estoque"])

        messages.success(
            request,
            "Venda registrada e conta a receber criada com sucesso!",
        )
        return redirect("vendas")

    return render(
        request,
        "cadastrar_venda.html",
        {
            "pessoas": pessoas_lista,
            "produtos": produtos_lista,
        },
    )


def excluir_venda(request, id):
    venda = get_object_or_404(
        Venda.objects.select_related("produto", "pessoa"),
        id=id,
    )

    if request.method == "POST":
        produto = venda.produto
        produto.estoque += venda.quantidade
        produto.save(update_fields=["estoque"])

        venda.delete()

        messages.success(
            request,
            "Venda cancelada e estoque restaurado com sucesso!",
        )
        return redirect("vendas")

    return render(
        request,
        "excluir_venda.html",
        {"venda": venda},
    )


# =========================
# CONTAS A RECEBER
# =========================

def contas_receber(request):
    contas = ContaReceber.objects.select_related(
        "venda",
        "venda__pessoa",
        "venda__produto",
    ).order_by("-vencimento")

    return render(
        request,
        "contas_receber.html",
        {"contas": contas},
    )
