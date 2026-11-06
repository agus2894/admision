from django import forms

from .models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'dni', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'cobertura_medica', 'contacto_emergencia', 'telefono_contacto',
            'alergias_conocidas', 'antecedentes_patologicos',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'alergias_conocidas': forms.Textarea(attrs={'rows': 2}),
            'antecedentes_patologicos': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css

