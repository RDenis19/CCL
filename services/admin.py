# Archivo: services/admin.py

from django.contrib import admin

from .models import (
    CategoriaServicio, Servicio, DetalleCobertura, Convenio, Beneficio,
    DetalleBeneficio, RecursoServicio, HorarioDisponible, SolicitudServicio
)


# --- INLINES ---
class DetalleCoberturaInline(admin.TabularInline):
    model = DetalleCobertura
    extra = 1


class RecursoServicioInline(admin.TabularInline):
    model = RecursoServicio
    extra = 1


class DetalleBeneficioInline(admin.TabularInline):
    model = DetalleBeneficio
    extra = 1


# --- MODEL ADMINS ---
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("nombre", "descripcion")
    inlines = [DetalleCoberturaInline, RecursoServicioInline]


@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ("__str__", "convenio", "categoria")
    list_filter = ("categoria", "convenio")
    search_fields = ("descripcion",)
    inlines = [DetalleBeneficioInline]


@admin.register(SolicitudServicio)
class SolicitudServicioAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ("__str__", "estado", "fecha_creacion", "gestor")
    list_filter = ("estado", "recurso__servicio")
    search_fields = ("solicitante__username", "recurso__nombre")
    autocomplete_fields = ('solicitante', 'recurso', 'gestor')


@admin.register(RecursoServicio)
class RecursoServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'servicio', 'tipo')
    list_filter = ('tipo', 'servicio')
    search_fields = ('nombre', 'servicio__nombre')
    autocomplete_fields = ('servicio', 'responsable')


@admin.register(HorarioDisponible)
class HorarioDisponibleAdmin(admin.ModelAdmin):
    list_display = ('recurso', 'fecha_hora_inicio', 'fecha_hora_fin', 'esta_reservado')
    list_filter = ('esta_reservado',)
    search_fields = ('recurso__nombre',)
    autocomplete_fields = ('recurso',)


# --- REGISTROS SIMPLES ---
# Se registran los modelos que no necesitan una clase Admin personalizada.
admin.site.register(CategoriaServicio)
admin.site.register(Convenio)
