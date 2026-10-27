from django import forms

from .models import MetaEstudo, RegistroEstudo


class RegistroEstudoForm(forms.ModelForm):
    class Meta:
        model = RegistroEstudo
        fields = ["titulo", "assunto", "data", "reflexao", "tempo_estudado", "visibilidade"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "reflexao": forms.Textarea(attrs={"rows": 6}),
        }


class MetaEstudoForm(forms.ModelForm):
    class Meta:
        model = MetaEstudo
        fields = ["descricao", "progresso"]
