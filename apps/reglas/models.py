from django.conf import settings
from django.db import models


class Regla(models.Model):
    NIVEL_ALERTA_CHOICES = [
        ('CRITICA', 'Crítica (Rojo - Requiere Acción Inmediata)'),
        ('ADVERTENCIA', 'Advertencia (Amarillo - Monitoreo Estricto)'),
        ('INFO', 'Sugerencia / Informativa (Azul - Cuidados de Enfermería)'),
    ]

    codigo = models.SlugField('Código Identificador', unique=True)
    nombre = models.CharField('Nombre de la Regla', max_length=150)
    descripcion = models.TextField('Descripción Clínica / Justificación', blank=True)
    nivel_alerta = models.CharField(
        'Nivel de Alerta', max_length=15, choices=NIVEL_ALERTA_CHOICES, default='ADVERTENCIA',
    )
    titulo_alerta = models.CharField('Título de la Alerta', max_length=150)
    mensaje = models.TextField('Mensaje Descriptivo del Problema')
    sugerencia = models.TextField('Sugerencia de Cuidados / Protocolo Recomendado')
    condiciones = models.JSONField(
        'Condiciones Lógicas (JSON)',
        help_text=(
            'Estructura de evaluación: {"match": "ALL"|"ANY", '
            '"conditions": [{"field": "codigo_item", "operator": "==", "value": "val"}]}'
        ),
    )
    orden_prioridad = models.PositiveIntegerField('Prioridad de Visualización', default=100)
    activa = models.BooleanField('Activa', default=True)
    creada_el = models.DateTimeField(auto_now_add=True)
    actualizada_el = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Regla Clínica'
        verbose_name_plural = 'Reglas Clínicas'
        ordering = ['orden_prioridad', 'codigo']

    def __str__(self):
        return self.nombre


class AlertaGenerada(models.Model):
    NIVEL_CHOICES = [
        ('CRITICA', 'Crítica'),
        ('ADVERTENCIA', 'Advertencia'),
        ('INFO', 'Informativa'),
    ]

    admision = models.ForeignKey(
        'admisiones.Admision', on_delete=models.CASCADE, related_name='alertas',
    )
    regla = models.ForeignKey(
        Regla, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertas_emitidas',
    )
    codigo_regla = models.CharField('Código de Regla', max_length=60)
    nivel = models.CharField('Nivel', max_length=15, choices=NIVEL_CHOICES)
    titulo = models.CharField('Título', max_length=150)
    mensaje = models.TextField('Mensaje')
    sugerencia = models.TextField('Sugerencia')
    reconocida = models.BooleanField('Reconocida por Enfermería', default=False)
    reconocida_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='alertas_reconocidas',
    )
    fecha_generacion = models.DateTimeField('Fecha y Hora', auto_now_add=True)

    class Meta:
        verbose_name = 'Alerta Generada'
        verbose_name_plural = 'Alertas Generadas'
        ordering = ['-fecha_generacion']

    def __str__(self):
        return f'{self.titulo} ({self.get_nivel_display()})'
