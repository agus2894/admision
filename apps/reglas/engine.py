"""Motor de reglas clínicas.

Evalúa las respuestas del checklist de una Admision contra las reglas activas
y genera AlertaGenerada cuando una regla se cumple.

Formato esperado de `Regla.condiciones`:
    {
        "match": "ALL" | "ANY",
        "conditions": [
            {"field": "codigo_item", "operator": "==", "value": "valor"}
        ]
    }
Operadores soportados: ==, !=, >, >=, <, <=, in, contains.
"""
from .models import AlertaGenerada, Regla


def _castear_valor(item, valor_str):
    """Convierte el valor de texto guardado según el tipo de dato del ítem."""
    if valor_str in (None, ''):
        return None
    if item.tipo_dato == 'BOOLEAN':
        return valor_str.strip().lower() in ('true', '1', 'si', 'sí', 'yes')
    if item.tipo_dato == 'NUMBER':
        try:
            return float(valor_str)
        except (TypeError, ValueError):
            return None
    return valor_str


_OPERADORES = {
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '>': lambda a, b: a is not None and a > b,
    '>=': lambda a, b: a is not None and a >= b,
    '<': lambda a, b: a is not None and a < b,
    '<=': lambda a, b: a is not None and a <= b,
    'in': lambda a, b: a in b,
    'contains': lambda a, b: a is not None and b in a,
}


def _evaluar_condicion(condicion, valores):
    campo = condicion.get('field')
    operador = condicion.get('operator', '==')
    esperado = condicion.get('value')
    if campo not in valores or operador not in _OPERADORES:
        return False
    try:
        return _OPERADORES[operador](valores[campo], esperado)
    except TypeError:
        return False


def _regla_cumple(regla, valores):
    conditions = regla.condiciones.get('conditions', [])
    if not conditions:
        return False
    match = regla.condiciones.get('match', 'ALL').upper()
    resultados = (_evaluar_condicion(c, valores) for c in conditions)
    return all(resultados) if match == 'ALL' else any(resultados)


def obtener_valores_admision(admision):
    """Devuelve {codigo_item: valor_casteado} con las respuestas actuales."""
    valores = {}
    for respuesta in admision.respuestas.select_related('item').all():
        valores[respuesta.item.codigo] = _castear_valor(respuesta.item, respuesta.valor)
    return valores


def evaluar_admision(admision):
    """Evalúa todas las reglas activas contra la admisión y crea las alertas nuevas.

    Devuelve la lista de AlertaGenerada creadas en esta ejecución (no repite
    una alerta ya emitida para la misma regla en la misma admisión).
    """
    valores = obtener_valores_admision(admision)
    nuevas_alertas = []
    for regla in Regla.objects.filter(activa=True):
        if not _regla_cumple(regla, valores):
            continue
        alerta, creada = AlertaGenerada.objects.get_or_create(
            admision=admision,
            codigo_regla=regla.codigo,
            defaults={
                'regla': regla,
                'nivel': regla.nivel_alerta,
                'titulo': regla.titulo_alerta,
                'mensaje': regla.mensaje,
                'sugerencia': regla.sugerencia,
            },
        )
        if creada:
            nuevas_alertas.append(alerta)
    return nuevas_alertas
