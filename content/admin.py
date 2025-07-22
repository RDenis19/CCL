from django.contrib import admin

from .models import CategoriaNoticia, Noticia, ComentarioNoticia


@admin.register(CategoriaNoticia)
class CategoriaNoticiaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo CategoriaNoticia.
    Permite gestionar las categorías de las noticias.
    """
    list_display = ("nombre", "slug")
    # Facilita la creación del 'slug' automáticamente a partir del 'nombre'.
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ("nombre",)


class ComentarioNoticiaInline(admin.TabularInline):
    """
    Permite ver y gestionar los comentarios directamente desde la página
    de edición de una Noticia. 'TabularInline' los muestra en un formato
    de tabla compacto.
    """
    model = ComentarioNoticia
    extra = 0
    readonly_fields = ('autor', 'contenido', 'fecha_creacion')


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Noticia.
    Define la interfaz para crear, editar y gestionar los artículos.
    """
    list_display = ("titulo", "autor", "categoria", "estado", "fecha_publicacion")
    list_filter = ("estado", "categoria", "fecha_publicacion")
    search_fields = ("titulo", "contenido", "autor__username")
    prepopulated_fields = {"slug": ("titulo",)}
    autocomplete_fields = ('autor', 'categoria')
    inlines = [ComentarioNoticiaInline]


@admin.register(ComentarioNoticia)
class ComentarioNoticiaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo ComentarioNoticia.
    Permite la moderación de los comentarios de forma independiente.
    """
    list_display = ('autor', 'noticia', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ('autor__username', 'contenido', 'noticia__titulo')
