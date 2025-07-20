# Archivo: content/admin.py

from django.contrib import admin
from .models import CategoriaNoticia, Noticia, ComentarioNoticia


@admin.register(CategoriaNoticia)
class CategoriaNoticiaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ("nombre",)


class ComentarioNoticiaInline(admin.TabularInline):
    model = ComentarioNoticia
    extra = 0
    readonly_fields = ('autor', 'contenido', 'fecha_creacion')


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "estado", "fecha_publicacion")
    list_filter = ("estado", "categoria", "fecha_publicacion")
    search_fields = ("titulo", "contenido", "autor__username")
    prepopulated_fields = {"slug": ("titulo",)}
    autocomplete_fields = ('autor', 'categoria')
    inlines = [ComentarioNoticiaInline]


@admin.register(ComentarioNoticia)
class ComentarioNoticiaAdmin(admin.ModelAdmin):
    list_display = ('autor', 'noticia', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ('autor__username', 'contenido', 'noticia__titulo')
