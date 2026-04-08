from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from .api_views import OrdemDeServicoViewSet, ComprasViewSet, EmpresaViewSet, ObterTokenView

router = DefaultRouter()
router.register(r'ordens',   OrdemDeServicoViewSet, basename='api-ordens')
router.register(r'compras',  ComprasViewSet,         basename='api-compras')
router.register(r'empresas', EmpresaViewSet,         basename='api-empresas')

urlpatterns = [
    # Autenticação
    path('auth/token/', ObterTokenView.as_view(), name='api-token'),

    # Recursos
    path('', include(router.urls)),

    # Documentação OpenAPI
    path('schema/',       SpectacularAPIView.as_view(),    name='api-schema'),
    path('docs/',         SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-swagger-ui'),
    path('docs/redoc/',   SpectacularRedocView.as_view(url_name='api-schema'),   name='api-redoc'),
]
