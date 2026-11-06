from django.urls import path

from . import views

app_name = 'admisiones'

urlpatterns = [
    path('', views.historial, name='historial'),
    path('nueva/', views.nueva_admision, name='nueva_admision'),
    path('<int:pk>/', views.detalle_admision, name='detalle_admision'),
    path('<int:pk>/imprimir/', views.imprimir_resumen, name='imprimir_resumen'),
    path('<int:pk>/checklist/', views.guardar_checklist, name='guardar_checklist'),
    path('<int:pk>/alertas/<int:alerta_id>/reconocer/', views.reconocer_alerta, name='reconocer_alerta'),
]
