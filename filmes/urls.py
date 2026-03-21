from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    FilmeViewSet,
    GeneroViewSet,
    AvaliacaoViewSet,
    listar_filmes,
    detalhe_filme,
    criar_filme,
    editar_filme,
    excluir_filme,
    importar_filme_omdb,
)

router = DefaultRouter()
router.register(r'filmes', FilmeViewSet)
router.register(r'generos', GeneroViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)

urlpatterns = router.urls + [
    path('listar-filmes/', listar_filmes, name='listar_filmes'),
    path('filme/<int:id>/', detalhe_filme, name='detalhe_filme'),
    path('criar-filme/', criar_filme, name='criar_filme'),
    path('editar-filme/<int:id>/', editar_filme, name='editar_filme'),
    path('excluir-filme/<int:id>/', excluir_filme, name='excluir_filme'),
    path('importar-filme/', importar_filme_omdb, name='importar_filme_omdb'),
]