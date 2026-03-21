from rest_framework import viewsets
from .models import Filme
from .serializers import FilmeSerializer

class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer