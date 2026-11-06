from django import forms

from .models import Admision, ItemChecklist


class AdmisionForm(forms.ModelForm):
    class Meta:
        model = Admision
        fields = [
            'cama', 'procedencia', 'diagnostico_ingreso', 'motivo_ingreso',
        ]
        widgets = {
            'motivo_ingreso': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css


def campo_para_item(item):
    """Devuelve el forms.Field adecuado según el tipo de dato del ítem."""
    etiqueta = item.etiqueta
    ayuda = item.ayuda
    if item.tipo_dato == 'BOOLEAN':
        return forms.ChoiceField(
            label=etiqueta, help_text=ayuda, required=False,
            choices=[('', '---'), ('true', 'Sí'), ('false', 'No')],
            widget=forms.Select(attrs={'class': 'form-select'}),
        )
    if item.tipo_dato == 'CHOICE':
        opciones = [(op, op) for op in (item.opciones or [])]
        return forms.ChoiceField(
            label=etiqueta, help_text=ayuda, required=False,
            choices=[('', '---')] + opciones,
            widget=forms.Select(attrs={'class': 'form-select'}),
        )
    if item.tipo_dato == 'NUMBER':
        return forms.FloatField(
            label=etiqueta, help_text=ayuda, required=False,
            widget=forms.NumberInput(attrs={
                'placeholder': item.placeholder, 'step': 'any', 'class': 'form-control',
            }),
        )
    return forms.CharField(
        label=etiqueta, help_text=ayuda, required=False,
        widget=forms.TextInput(attrs={'placeholder': item.placeholder, 'class': 'form-control'}),
    )


class ChecklistForm(forms.Form):
    """Formulario dinámico construido a partir de los ItemChecklist activos."""

    def __init__(self, *args, admision=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.admision = admision
        items = ItemChecklist.objects.filter(activo=True).select_related('categoria')
        respuestas_actuales = {}
        if admision is not None:
            respuestas_actuales = {
                r.item_id: r.valor for r in admision.respuestas.all()
            }
        for item in items:
            nombre_campo = f'item_{item.id}'
            self.fields[nombre_campo] = campo_para_item(item)
            if item.id in respuestas_actuales:
                self.fields[nombre_campo].initial = respuestas_actuales[item.id]

    def items_agrupados(self):
        """Devuelve [(categoria, [bound_field, ...]), ...] para renderizar por categoría."""
        items = ItemChecklist.objects.filter(activo=True).select_related('categoria')
        grupos = {}
        for item in items:
            grupos.setdefault(item.categoria, []).append(self[f'item_{item.id}'])
        return sorted(grupos.items(), key=lambda g: (g[0].orden, g[0].nombre))

    def guardar(self, admision):
        from .models import RespuestaChecklist

        for nombre_campo, valor in self.cleaned_data.items():
            item_id = int(nombre_campo.split('_', 1)[1])
            RespuestaChecklist.objects.update_or_create(
                admision=admision, item_id=item_id,
                defaults={'valor': '' if valor is None else str(valor)},
            )
