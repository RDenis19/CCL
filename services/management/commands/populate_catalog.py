# Archivo: services/management/commands/populate_catalog.py

import json
from django.core.management.base import BaseCommand
from services.models import (
    CategoriaServicio, Servicio, DetalleCobertura, RecursoServicio,
    Convenio, Beneficio, DetalleBeneficio
)


class Command(BaseCommand):
    help = 'Limpia y puebla la base de datos con el catálogo completo de servicios y convenios.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Iniciando Carga de Catálogo Completo ---"))
        self._populate_servicios()
        self._populate_convenios()
        self.stdout.write(self.style.SUCCESS("--- Proceso de Carga Finalizado con Éxito ---"))

    def _populate_servicios(self):
        self.stdout.write(self.style.WARNING("\n1. Poblando Servicios Internos..."))

        # Limpieza
        Servicio.objects.all().delete()
        CategoriaServicio.objects.all().delete()

        datos_json = """
        {
          "servicios": [
            {"nombre": "Seguro de Vida", "descripcion": "Cobertura de vida colectiva para socios.", "categoria": "Seguros", "coberturas": {"Muerte por cualquier causa": 8000, "Incapacidad total y permanente": 8000, "Gastos de sepelio": 1500}},
            {"nombre": "Áreas Deportivas", "descripcion": "Espacios recreativos y deportivos.", "categoria": "Recreación", "instalaciones": ["Cancha de fútbol 5", "Cancha de ecuavóley 1", "Cancha de ecuavóley 2", "Zona húmeda"]},
            {"nombre": "Salones Sociales", "descripcion": "Alquiler de salones para eventos.", "categoria": "Eventos", "salones": [{"nombre": "Salón Arsenio Vivanco"}, {"nombre": "Salón Alonso de Mercadillo"}]},
            {"nombre": "Atención Médica Gratuita", "descripcion": "Consultas médicas básicas sin costo.", "categoria": "Salud", "instalaciones": ["Médico General 1"]},
            {"nombre": "Asesorías sin costo", "descripcion": "Orientación profesional legal y empresarial.", "categoria": "Consultoría", "instalaciones": ["Asesor Legal", "Asesor Laboral"]},
            {"nombre": "Firma Electrónica", "descripcion": "Emisión de certificados de firma electrónica.", "categoria": "Tecnología", "instalaciones": ["Punto de Emisión"]}
          ]
        }
        """
        data = json.loads(datos_json)
        CATEGORIAS_TIPO_PERSONA = ["Salud", "Consultoría", "Tecnología"]

        for item in data['servicios']:
            cat, _ = CategoriaServicio.objects.get_or_create(nombre=item['categoria'])
            svc = Servicio.objects.create(categoria=cat, nombre=item['nombre'], descripcion=item['descripcion'])
            self.stdout.write(f"  -> Servicio: '{svc.nombre}'")

            tipo_recurso = RecursoServicio.TipoRecurso.PERSONA if cat.nombre in CATEGORIAS_TIPO_PERSONA else RecursoServicio.TipoRecurso.FISICO

            for cob in item.get('coberturas', {}).items():
                DetalleCobertura.objects.create(servicio=svc, nombre_cobertura=cob[0], valor=cob[1])
            for inst in item.get('instalaciones', []):
                RecursoServicio.objects.create(servicio=svc, nombre=inst, tipo=tipo_recurso)
            for salon in item.get('salones', []):
                RecursoServicio.objects.create(servicio=svc, nombre=salon['nombre'],
                                               tipo=RecursoServicio.TipoRecurso.FISICO)

        self.stdout.write(self.style.SUCCESS("Servicios poblados con éxito."))

    def _populate_convenios(self):
        self.stdout.write(self.style.WARNING("\n2. Poblando Convenios y Beneficios..."))

        # Limpieza
        Convenio.objects.all().delete()

        datos_json = """
        {
          "beneficios": {
            "salud": [
              {"entidad": "SOLCA", "categoria": "Salud", "descripcion": "Red oncológica con tarifas preferenciales.", "descuentos": ["10% UCI adulto/neonatal", "10% quirófano, emergencia, hospitalización"]},
              {"entidad": "Centro Médico Xpertos", "categoria": "Salud", "descripcion": "Clínica integral con laboratorio.", "descuentos": ["5% laboratorio clínico", "10% consultas y procedimientos"]}
            ],
            "empresas": [
              {"entidad": "Security Data", "categoria": "Empresarial", "descripcion": "Soluciones legales y de protección de datos.", "descuentos": ["60% en contratos y asesorías"]},
              {"entidad": "OPE Corporation", "categoria": "Empresarial", "descripcion": "Consultora para certificaciones ISO.", "descuentos": ["20% en certificaciones ISO"]}
            ],
            "educacion": [
              {"entidad": "Universidad Nacional de Loja", "categoria": "Educación", "descripcion": "Universidad pública con becas.", "descuentos": ["20% beca en maestrías"]}
            ]
          }
        }
        """
        data = json.loads(datos_json)

        for categoria_nombre, convenios_lista in data.get('beneficios', {}).items():
            for item in convenios_lista:
                cat_str = item['categoria'].capitalize()
                cat, _ = CategoriaServicio.objects.get_or_create(nombre=cat_str)

                conv = Convenio.objects.create(nombre_entidad=item['entidad'], contacto=item.get('contacto', ''))
                self.stdout.write(f"  -> Convenio: '{conv.nombre_entidad}'")

                ben = Beneficio.objects.create(convenio=conv, categoria=cat, descripcion=item['descripcion'])

                for desc in item.get('descuentos', []):
                    DetalleBeneficio.objects.create(beneficio=ben, descripcion_descuento=desc)

        self.stdout.write(self.style.SUCCESS("Convenios poblados con éxito."))
