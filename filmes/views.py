from django.shortcuts import render, redirect
from rest_framework import viewsets

from .models import Filme, Genero, Avaliacao
from .serializers import FilmeSerializer, GeneroSerializer, AvaliacaoSerializer


class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer


def criar_filme(request):
    generos = Genero.objects.all()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        ano = request.POST.get('ano')
        duracao = request.POST.get('duracao')
        nota_media = request.POST.get('nota_media')
        poster_url = request.POST.get('poster_url')

        filme = Filme.objects.create(
            titulo=titulo,
            descricao=descricao,
            ano=ano,
            duracao=duracao or None,
            nota_media=nota_media or None,
            poster_url=poster_url or None
        )

        generos_ids = request.POST.getlist('generos')
        filme.generos.set(generos_ids)

        return redirect('/filmes/')

    return render(request, 'filmes/criar_filme.html', {'generos': generos})