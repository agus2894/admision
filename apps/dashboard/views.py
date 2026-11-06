from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from apps.admisiones.models import Admision
from apps.pacientes.models import Paciente
from apps.reglas.models import AlertaGenerada


@login_required
def metricas(request):
    admisiones_por_procedencia = (
        Admision.objects.values('procedencia').annotate(total=Count('id')).order_by('-total')
    )
    contexto = {
        'total_pacientes': Paciente.objects.count(),
        'admisiones_activas': Admision.objects.filter(estado='ACTIVA').count(),
        'admisiones_totales': Admision.objects.count(),
        'alertas_criticas_pendientes': AlertaGenerada.objects.filter(
            nivel='CRITICA', reconocida=False,
        ).count(),
        'alertas_pendientes_total': AlertaGenerada.objects.filter(reconocida=False).count(),
        'admisiones_por_procedencia': admisiones_por_procedencia,
        'ultimas_alertas': AlertaGenerada.objects.select_related('admision__paciente').filter(
            reconocida=False,
        )[:10],
    }
    return render(request, 'dashboard/metricas.html', contexto)
