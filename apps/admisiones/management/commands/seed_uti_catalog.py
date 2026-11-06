from django.core.management.base import BaseCommand

from apps.admisiones.models import CategoriaItem, ItemChecklist

CATALOGO = [
    {
        'categoria': {'codigo': 'hemodinamia', 'nombre': 'Hemodinamia', 'icono': 'bi-heart-pulse', 'orden': 1},
        'items': [
            {'codigo': 'presion_arterial', 'etiqueta': 'Presión Arterial', 'tipo_dato': 'TEXT', 'unidad': 'mmHg', 'placeholder': '120/80', 'es_critico': True},
            {'codigo': 'frecuencia_cardiaca', 'etiqueta': 'Frecuencia Cardíaca', 'tipo_dato': 'NUMBER', 'unidad': 'lpm', 'es_critico': True},
            {'codigo': 'perfusion_periferica', 'etiqueta': 'Perfusión Periférica', 'tipo_dato': 'CHOICE', 'opciones': ['Normal', 'Enlentecida', 'Ausente']},
        ],
    },
    {
        'categoria': {'codigo': 'respiratorio', 'nombre': 'Respiratorio', 'icono': 'bi-lungs', 'orden': 2},
        'items': [
            {'codigo': 'saturacion_o2', 'etiqueta': 'Saturación de Oxígeno', 'tipo_dato': 'NUMBER', 'unidad': '%', 'es_critico': True},
            {'codigo': 'frecuencia_respiratoria', 'etiqueta': 'Frecuencia Respiratoria', 'tipo_dato': 'NUMBER', 'unidad': 'rpm', 'es_critico': True},
            {'codigo': 'via_aerea_artificial', 'etiqueta': '¿Vía Aérea Artificial?', 'tipo_dato': 'BOOLEAN'},
        ],
    },
    {
        'categoria': {'codigo': 'neurologico', 'nombre': 'Neurológico', 'icono': 'bi-activity', 'orden': 3},
        'items': [
            {'codigo': 'glasgow', 'etiqueta': 'Escala de Glasgow', 'tipo_dato': 'NUMBER', 'es_critico': True},
            {'codigo': 'sedacion', 'etiqueta': '¿Bajo Sedación?', 'tipo_dato': 'BOOLEAN'},
        ],
    },
    {
        'categoria': {'codigo': 'temperatura', 'nombre': 'Temperatura', 'icono': 'bi-thermometer-half', 'orden': 4},
        'items': [
            {'codigo': 'temperatura_corporal', 'etiqueta': 'Temperatura Corporal', 'tipo_dato': 'NUMBER', 'unidad': '°C', 'es_critico': True},
        ],
    },
    {
        'categoria': {'codigo': 'piel_heridas', 'nombre': 'Piel y Heridas', 'icono': 'bi-bandaid', 'orden': 5},
        'items': [
            {'codigo': 'lesiones_por_presion', 'etiqueta': '¿Lesiones por Presión?', 'tipo_dato': 'BOOLEAN'},
            {'codigo': 'estado_heridas', 'etiqueta': 'Estado de Heridas/Sitios Quirúrgicos', 'tipo_dato': 'CHOICE', 'opciones': ['Sin heridas', 'Limpia', 'Con signos de infección']},
        ],
    },
]


class Command(BaseCommand):
    help = 'Carga (o actualiza) el catálogo de categorías e ítems de checklist clínico de UTI.'

    def handle(self, *args, **options):
        total_categorias = 0
        total_items = 0
        for bloque in CATALOGO:
            categoria, creada = CategoriaItem.objects.update_or_create(
                codigo=bloque['categoria']['codigo'],
                defaults=bloque['categoria'],
            )
            total_categorias += 1
            for orden, item_data in enumerate(bloque['items']):
                item_data = {**item_data, 'orden': orden}
                item_data.setdefault('opciones', [])
                ItemChecklist.objects.update_or_create(
                    codigo=item_data['codigo'],
                    defaults={**item_data, 'categoria': categoria},
                )
                total_items += 1

        self.stdout.write(self.style.SUCCESS(
            f'Catálogo cargado: {total_categorias} categorías, {total_items} ítems.'
        ))
