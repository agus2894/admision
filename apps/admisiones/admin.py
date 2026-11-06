from django.contrib import admin

from .models import Admision, CategoriaItem, ItemChecklist, RespuestaChecklist


class RespuestaChecklistInline(admin.TabularInline):
    model = RespuestaChecklist
    extra = 0


@admin.register(Admision)
class AdmisionAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'cama', 'procedencia', 'estado', 'fecha_ingreso', 'enfermero_responsable')
    list_filter = ('estado', 'procedencia')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'paciente__dni', 'cama', 'diagnostico_ingreso')
    date_hierarchy = 'fecha_ingreso'
    inlines = [RespuestaChecklistInline]


class ItemChecklistInline(admin.TabularInline):
    model = ItemChecklist
    extra = 0


@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'orden')
    prepopulated_fields = {'codigo': ('nombre',)}
    inlines = [ItemChecklistInline]


@admin.register(ItemChecklist)
class ItemChecklistAdmin(admin.ModelAdmin):
    list_display = ('etiqueta', 'codigo', 'categoria', 'tipo_dato', 'es_critico', 'activo')
    list_filter = ('categoria', 'tipo_dato', 'es_critico', 'activo')
    prepopulated_fields = {'codigo': ('etiqueta',)}
