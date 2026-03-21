from django.db import models


class Genero(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    ano = models.IntegerField()
    duracao = models.IntegerField(help_text="Duração em minutos", null=True, blank=True)
    nota_media = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    generos = models.ManyToManyField(Genero, related_name='filmes')

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='avaliacoes')
    nome_usuario = models.CharField(max_length=100)
    nota = models.IntegerField()
    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome_usuario} - {self.filme.titulo}'