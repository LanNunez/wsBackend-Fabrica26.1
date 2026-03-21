from rest_framework import serializers
from .models import Filme, Genero, Avaliacao


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'


class FilmeSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)
    avaliacoes = AvaliacaoSerializer(many=True, read_only=True)
    generos_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genero.objects.all(),
        source='generos',
        write_only=True
    )

    class Meta:
        model = Filme
        fields = [
            'id',
            'titulo',
            'descricao',
            'ano',
            'duracao',
            'nota_media',
            'poster_url',
            'generos',
            'generos_ids',
            'avaliacoes',
        ]