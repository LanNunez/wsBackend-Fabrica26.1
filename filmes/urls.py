from rest_framework.routers import DefaultRouter
from .views import FilmeViewSet

router = DefaultRouter()
router.register(r'filmes', FilmeViewSet)

urlpatterns = router.urls