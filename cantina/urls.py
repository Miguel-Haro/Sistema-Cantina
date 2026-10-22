from django.contrib import admin
from django.urls import path
from produtos import views


urlpatterns = [
    # =========================
    # ADMIN
    # =========================
    path("admin/", admin.site.urls),

    # =========================
    # DASHBOARD
    # =========================
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    # =========================
    # PRODUTOS
    # =========================
    path(
        "produtos/",
        views.produtos,
        name="produtos",
    ),
    path(
        "produtos/adicionar/",
        views.cadastrar_produto,
        name="adicionar_produto",
    ),
    path(
        "produtos/editar/<int:id>/",
        views.editar_produto,
        name="editar_produto",
    ),
    path(
        "produtos/excluir/<int:id>/",
        views.excluir_produto,
        name="excluir_produto",
    ),

    # =========================
    # CATEGORIAS
    # =========================
    path(
        "categorias/",
        views.categorias,
        name="categorias",
    ),
    path(
        "categorias/adicionar/",
        views.adicionar_categoria,
        name="adicionar_categoria",
    ),
    path(
        "categorias/editar/<int:id>/",
        views.editar_categoria,
        name="editar_categoria",
    ),
    path(
        "categorias/excluir/<int:id>/",
        views.excluir_categoria,
        name="excluir_categoria",
    ),

    # =========================
    # PESSOAS
    # =========================
    path(
        "pessoas/",
        views.pessoas,
        name="pessoas",
    ),
    path(
        "pessoas/adicionar/",
        views.cadastrar_pessoa,
        name="adicionar_pessoa",
    ),
    path(
        "pessoas/editar/<int:id>/",
        views.editar_pessoa,
        name="editar_pessoa",
    ),
    path(
        "pessoas/excluir/<int:id>/",
        views.excluir_pessoa,
        name="excluir_pessoa",
    ),

    # =========================
    # VENDAS
    # =========================
    path(
        "vendas/",
        views.vendas,
        name="vendas",
    ),
    path(
        "vendas/cadastrar/",
        views.cadastrar_venda,
        name="cadastrar_venda",
    ),
    path(
        "vendas/excluir/<int:id>/",
        views.excluir_venda,
        name="excluir_venda",
    ),

    # =========================
    # CONTAS A RECEBER
    # =========================
    path(
        "contas-receber/",
        views.contas_receber,
        name="contas_receber",
    ),
]
