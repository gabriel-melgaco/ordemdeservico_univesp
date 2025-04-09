from django.urls import path
from .views import home, home_ordem, home_compras, criar_ordem, listar_ordens, executar_ordem, finalizar_ordem, detalhar_ordem, buscar_por_numero, filtrar_por_periodo, listar_compras, atualizar_compra

urlpatterns = [
    path('', home, name='home'),  # URL da página inicial
    path('indexordem/', home_ordem, name='home_ordem'),  # URL da página ordens
    path('indexcompras/', home_compras, name='home_compras'),  # URL da página Compras
    path('criar/', criar_ordem, name='criar_ordem'),
    path('listar/', listar_ordens, name='listar_ordens'),
    path('<int:pk>/executar/', executar_ordem, name='executar_ordem'),
    path('<int:pk>/finalizar/', finalizar_ordem, name='finalizar_ordem'),
    path('<int:pk>/', detalhar_ordem, name='detalhar_ordem'),
    path('buscar_por_numero/', buscar_por_numero, name='buscar_por_numero'),
    path('filtrar_por_periodo/', filtrar_por_periodo, name='filtrar_por_periodo'),
    path('compras/', listar_compras, name='listar_compras'),
    path('compras/<int:pk>/atualizar/', atualizar_compra, name='atualizar_compra'),
]
