from django.contrib import admin
from .models import Filme

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano', 'nota_media')
    search_fields = ('titulo',)
    list_filter = ('ano',)