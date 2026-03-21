from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FilmeViewSet, GeneroViewSet, AvaliacaoViewSet, criar_filme

router = DefaultRouter()
router.register(r'filmes', FilmeViewSet)
router.register(r'generos', GeneroViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)

urlpatterns = router.urls + [
    path('criar-filme/', criar_filme, name='criar_filme'),
]