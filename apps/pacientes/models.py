from django.db import models


class Paciente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    dni = models.CharField(
        'DNI / Documento', max_length=20, unique=True, db_index=True,
    )
    nombre = models.CharField('Nombre(s)', max_length=100)
    apellido = models.CharField('Apellido(s)', max_length=100)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento')
    sexo = models.CharField(
        'Sexo biológico / Género', max_length=1, choices=SEXO_CHOICES, default='M',
    )
    cobertura_medica = models.CharField('Obra Social / Prepaga', max_length=120, blank=True)
    contacto_emergencia = models.CharField(
        'Contacto de Emergencia / Familiar', max_length=150, blank=True,
    )
    telefono_contacto = models.CharField('Teléfono', max_length=50, blank=True)
    alergias_conocidas = models.TextField(
        'Alergias Conocidas', blank=True,
        help_text='Ej: Penicilina, Látex, Yodo, Dipirona',
    )
    antecedentes_patologicos = models.TextField(
        'Antecedentes Patológicos', blank=True,
        help_text='Ej: HTA, DBT, EPOC, Insuficiencia Cardíaca, etc.',
    )
    fecha_registro = models.DateTimeField('Fecha de Registro', auto_now_add=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.apellido}, {self.nombre} (DNI {self.dni})'
