import os
import requests
from django.http import JsonResponse
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

def importar_filme_omdb(request):
    titulo = request.GET.get('titulo')

    if not titulo:
        return JsonResponse({'erro': 'Informe o título do filme.'}, status=400)

    api_key = os.getenv('OMDB_API_KEY')

    if not api_key:
        return JsonResponse({'erro': 'Chave OMDb não configurada.'}, status=500)

    # 1) tenta busca exata
    url = f'https://www.omdbapi.com/?apikey={api_key}&t={titulo}&plot=full'
    response = requests.get(url)
    data = response.json()

    # 2) se não encontrar, tenta busca ampla
    if data.get('Response') == 'False':
        search_url = f'https://www.omdbapi.com/?apikey={api_key}&s={titulo}'
        search_response = requests.get(search_url)
        search_data = search_response.json()

        if search_data.get('Response') == 'False':
            return JsonResponse({'erro': 'Filme não encontrado.'}, status=404)

        primeiro_resultado = search_data['Search'][0]['Title']

        url = f'https://www.omdbapi.com/?apikey={api_key}&t={primeiro_resultado}&plot=full'
        response = requests.get(url)
        data = response.json()

        if data.get('Response') == 'False':
            return JsonResponse({'erro': 'Filme não encontrado.'}, status=404)

    filme = Filme.objects.create(
        titulo=data.get('Title', ''),
        descricao=data.get('Plot', ''),
        ano=int(data.get('Year', '0').split('–')[0]) if data.get('Year') else 0,
        duracao=int(data.get('Runtime', '0 min').split()[0]) if data.get('Runtime') and data.get('Runtime') != 'N/A' else None,
        nota_media=float(data.get('imdbRating')) if data.get('imdbRating') and data.get('imdbRating') != 'N/A' else None,
        poster_url=data.get('Poster') if data.get('Poster') != 'N/A' else None
    )

    return JsonResponse({
        'mensagem': 'Filme importado com sucesso',
        'titulo': filme.titulo
    }, status=201)