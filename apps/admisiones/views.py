from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.pacientes.forms import PacienteForm
from apps.pacientes.models import Paciente
from apps.reglas.engine import evaluar_admision

from .forms import AdmisionForm, ChecklistForm
from .models import Admision


@login_required
def historial(request):
    admisiones = Admision.objects.select_related('paciente').all()
    estado = request.GET.get('estado', '')
    if estado:
        admisiones = admisiones.filter(estado=estado)
    return render(request, 'admisiones/historial.html', {
        'admisiones': admisiones,
        'estado_seleccionado': estado,
        'estados': Admision.ESTADO_CHOICES,
    })


@login_required
def nueva_admision(request):
    paciente = None
    if request.method == 'POST':
        dni = request.POST.get('dni', '').strip()
        paciente = Paciente.objects.filter(dni=dni).first()
        admision_form = AdmisionForm(request.POST)
        paciente_form = None if paciente else PacienteForm(request.POST)

        paciente_valido = paciente_form.is_valid() if paciente_form else True
        if paciente_valido and admision_form.is_valid():
            if paciente is None:
                paciente = paciente_form.save()
            admision = admision_form.save(commit=False)
            admision.paciente = paciente
            admision.enfermero_responsable = request.user
            admision.save()
            messages.success(request, 'Admisión registrada correctamente.')
            return redirect('admisiones:detalle_admision', pk=admision.pk)
        if paciente_form is None:
            paciente_form = PacienteForm(initial={'dni': dni})
    else:
        admision_form = AdmisionForm()
        paciente_form = PacienteForm()

    return render(request, 'admisiones/nueva_admision.html', {
        'admision_form': admision_form,
        'paciente_form': paciente_form,
    })


@login_required
def detalle_admision(request, pk):
    admision = get_object_or_404(Admision.objects.select_related('paciente'), pk=pk)
    checklist_form = ChecklistForm(admision=admision)
    alertas = admision.alertas.select_related('regla').all()
    return render(request, 'admisiones/detalle_admision.html', {
        'admision': admision,
        'checklist_form': checklist_form,
        'alertas': alertas,
    })


@login_required
@require_POST
def guardar_checklist(request, pk):
    admision = get_object_or_404(Admision, pk=pk)
    form = ChecklistForm(request.POST, admision=admision)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
    form.guardar(admision)
    nuevas_alertas = evaluar_admision(admision)
    return JsonResponse({
        'ok': True,
        'alertas_nuevas': [
            {
                'id': alerta.id,
                'nivel': alerta.nivel,
                'titulo': alerta.titulo,
                'mensaje': alerta.mensaje,
                'sugerencia': alerta.sugerencia,
            }
            for alerta in nuevas_alertas
        ],
    })


@login_required
@require_POST
def reconocer_alerta(request, pk, alerta_id):
    admision = get_object_or_404(Admision, pk=pk)
    alerta = get_object_or_404(admision.alertas, pk=alerta_id)
    alerta.reconocida = True
    alerta.reconocida_por = request.user
    alerta.save(update_fields=['reconocida', 'reconocida_por'])
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})
    return redirect('admisiones:detalle_admision', pk=pk)


@login_required
def imprimir_resumen(request, pk):
    admision = get_object_or_404(Admision.objects.select_related('paciente'), pk=pk)
    respuestas = admision.respuestas.select_related('item', 'item__categoria').all()
    alertas = admision.alertas.all()
    return render(request, 'admisiones/imprimir_resumen.html', {
        'admision': admision,
        'respuestas': respuestas,
        'alertas': alertas,
    })
