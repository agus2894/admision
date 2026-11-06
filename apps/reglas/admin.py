from django.contrib import admin

from .models import AlertaGenerada, Regla


@admin.register(Regla)
class ReglaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'nivel_alerta', 'orden_prioridad', 'activa')
    list_filter = ('nivel_alerta', 'activa')
    search_fields = ('codigo', 'nombre')
    prepopulated_fields = {'codigo': ('nombre',)}


@admin.register(AlertaGenerada)
class AlertaGeneradaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel', 'admision', 'reconocida', 'fecha_generacion')
    list_filter = ('nivel', 'reconocida')
    date_hierarchy = 'fecha_generacion'
