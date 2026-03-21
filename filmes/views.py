import os
import requests

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .models import Filme, Genero, Avaliacao
from .serializers import FilmeSerializer, GeneroSerializer, AvaliacaoSerializer


# =========================
# API REST (DRF)
# =========================

class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer

    # filtros e busca
    filterset_fields = ['ano', 'generos']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['ano', 'nota_media', 'titulo']


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer


# =========================
# HTML - LISTAGEM
# =========================

def listar_filmes(request):
    filmes = Filme.objects.all()
    return render(request, 'filmes/listar_filmes.html', {'filmes': filmes})


# =========================
# HTML - DETALHE
# =========================

def detalhe_filme(request, id):
    filme = get_object_or_404(Filme, id=id)
    return render(request, 'filmes/detalhe_filme.html', {'filme': filme})


# =========================
# HTML - CRIAR FILME
# =========================

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

        return redirect('listar_filmes')

    return render(request, 'filmes/criar_filme.html', {'generos': generos})


# =========================
# HTML - EDITAR FILME
# =========================

def editar_filme(request, id):
    filme = get_object_or_404(Filme, id=id)
    generos = Genero.objects.all()

    if request.method == 'POST':
        filme.titulo = request.POST.get('titulo')
        filme.descricao = request.POST.get('descricao')
        filme.ano = request.POST.get('ano')
        filme.duracao = request.POST.get('duracao') or None
        filme.nota_media = request.POST.get('nota_media') or None
        filme.poster_url = request.POST.get('poster_url') or None
        filme.save()

        generos_ids = request.POST.getlist('generos')
        filme.generos.set(generos_ids)

        return redirect('listar_filmes')

    return render(
        request,
        'filmes/editar_filme.html',
        {
            'filme': filme,
            'generos': generos
        }
    )


# =========================
# HTML - EXCLUIR FILME
# =========================

def excluir_filme(request, id):
    filme = get_object_or_404(Filme, id=id)

    if request.method == 'POST':
        filme.delete()
        return redirect('listar_filmes')

    return render(request, 'filmes/excluir_filme.html', {'filme': filme})


# =========================
# API EXTERNA - OMDb
# =========================

def importar_filme_omdb(request):
    titulo = request.GET.get('titulo')

    if not titulo:
        return JsonResponse({'erro': 'Informe o título do filme.'}, status=400)

    api_key = os.getenv('OMDB_API_KEY')

    if not api_key:
        return JsonResponse({'erro': 'Chave OMDb não configurada.'}, status=500)

    url = f'https://www.omdbapi.com/?apikey={api_key}&t={titulo}&plot=full'
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'False':
        return JsonResponse(
            {'erro': data.get('Error', 'Filme não encontrado.')},
            status=404
        )

    ano_bruto = data.get('Year', '')
    runtime_bruto = data.get('Runtime', '')
    nota_bruta = data.get('imdbRating', '')
    poster_bruto = data.get('Poster', '')

    ano = None
    if ano_bruto and ano_bruto != 'N/A':
        try:
            ano = int(ano_bruto.split('–')[0].split('-')[0])
        except ValueError:
            ano = 0

    duracao = None
    if runtime_bruto and runtime_bruto != 'N/A':
        try:
            duracao = int(runtime_bruto.split()[0])
        except ValueError:
            duracao = None

    nota_media = None
    if nota_bruta and nota_bruta != 'N/A':
        try:
            nota_media = float(nota_bruta)
        except ValueError:
            nota_media = None

    poster_url = None
    if poster_bruto and poster_bruto != 'N/A':
        poster_url = poster_bruto

    filme = Filme.objects.create(
        titulo=data.get('Title', ''),
        descricao=data.get('Plot', ''),
        ano=ano if ano is not None else 0,
        duracao=duracao,
        nota_media=nota_media,
        poster_url=poster_url
    )

    return JsonResponse(
        {
            'mensagem': 'Filme importado com sucesso.',
            'id': filme.id,
            'titulo': filme.titulo
        },
        status=201
    )