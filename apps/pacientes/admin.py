from django.contrib import admin

from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'apellido', 'nombre', 'fecha_nacimiento', 'sexo', 'cobertura_medica')
    search_fields = ('dni', 'nombre', 'apellido')
    list_filter = ('sexo',)
