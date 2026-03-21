from django.db import models

class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    ano = models.IntegerField()

    def __str__(self):
        return self.titulo