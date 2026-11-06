from django.conf import settings
from django.db import models
from django.utils import timezone


class Admision(models.Model):
    PROCEDENCIA_CHOICES = [
        ('GUARDIA', 'Guardia / Shockroom'),
        ('QUIROFANO', 'Quirófano / Recuperación'),
        ('PISO', 'Sala General / Internación'),
        ('DERIVACION', 'Derivación Externa / Otra Institución'),
    ]
    ESTADO_CHOICES = [
        ('ACTIVA', 'Internado en UTI'),
        ('ALTA', 'Alta de UTI'),
        ('DERIVADO', 'Derivado a otra área/centro'),
        ('OBITO', 'Óbito'),
    ]

    paciente = models.ForeignKey(
        'pacientes.Paciente', on_delete=models.CASCADE, related_name='admisiones',
    )
    enfermero_responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Enfermero/a Responsable',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='admisiones_registradas',
    )
    fecha_ingreso = models.DateTimeField('Fecha y Hora de Ingreso', default=timezone.now)
    cama = models.CharField('Cama / Unidad', max_length=30, help_text='Ej: Cama 04 - UTI')
    procedencia = models.CharField(
        'Procedencia', max_length=20, choices=PROCEDENCIA_CHOICES, default='GUARDIA',
    )
    diagnostico_ingreso = models.CharField('Diagnóstico de Ingreso', max_length=255)
    motivo_ingreso = models.TextField('Motivo de Ingreso / Resumen de Cuadro', blank=True)
    estado = models.CharField('Estado', max_length=15, choices=ESTADO_CHOICES, default='ACTIVA')
    observaciones_generales = models.TextField('Observaciones de Enfermería', blank=True)
    fecha_cierre = models.DateTimeField('Fecha de Cierre', null=True, blank=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Admisión'
        verbose_name_plural = 'Admisiones'
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f'{self.paciente} - {self.cama} ({self.get_estado_display()})'


class CategoriaItem(models.Model):
    nombre = models.CharField('Nombre de Categoría', max_length=100)
    codigo = models.SlugField('Código', unique=True)
    icono = models.CharField('Icono Bootstrap Icons', max_length=50, default='bi-clipboard2-pulse')
    descripcion = models.CharField('Descripción', max_length=255, blank=True)
    orden = models.PositiveIntegerField('Orden de Visualización', default=0)

    class Meta:
        verbose_name = 'Categoría de Checklist'
        verbose_name_plural = 'Categorías de Checklist'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class ItemChecklist(models.Model):
    TIPO_DATO_CHOICES = [
        ('BOOLEAN', 'Booleano (Sí / No)'),
        ('CHOICE', 'Selección Única (Opciones)'),
        ('NUMBER', 'Numérico'),
        ('TEXT', 'Texto Libre'),
    ]

    categoria = models.ForeignKey(CategoriaItem, on_delete=models.CASCADE, related_name='items')
    codigo = models.SlugField(
        'Código Identificador', unique=True,
        help_text='Clave única usada en el motor de reglas',
    )
    etiqueta = models.CharField('Etiqueta / Pregunta Clínica', max_length=150)
    tipo_dato = models.CharField(
        'Tipo de Dato', max_length=15, choices=TIPO_DATO_CHOICES, default='CHOICE',
    )
    opciones = models.JSONField(
        'Opciones Disponibles', blank=True, default=list,
        help_text='Lista de valores posibles en formato JSON. Ej: ["Normal", "Disnea", "Taquipnea"]',
    )
    unidad = models.CharField('Unidad de Medida', max_length=20, blank=True, help_text='Ej: mmHg, lpm, °C')
    valor_por_defecto = models.CharField('Valor por Defecto', max_length=100, blank=True)
    placeholder = models.CharField('Placeholder / Sugerencia', max_length=150, blank=True)
    ayuda = models.CharField('Texto de Ayuda Clínica', max_length=255, blank=True)
    orden = models.PositiveIntegerField('Orden', default=0)
    es_critico = models.BooleanField('¿Parámetro Crítico?', default=False)
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Ítem de Checklist'
        verbose_name_plural = 'Ítems de Checklist'
        ordering = ['categoria__orden', 'orden', 'etiqueta']

    def __str__(self):
        return self.etiqueta


class RespuestaChecklist(models.Model):
    admision = models.ForeignKey(Admision, on_delete=models.CASCADE, related_name='respuestas')
    item = models.ForeignKey(ItemChecklist, on_delete=models.CASCADE, related_name='respuestas')
    valor = models.TextField('Valor Registrado', blank=True)

    class Meta:
        verbose_name = 'Respuesta de Checklist'
        verbose_name_plural = 'Respuestas de Checklist'
        unique_together = (('admision', 'item'),)

    def __str__(self):
        return f'{self.item.codigo}={self.valor}'
