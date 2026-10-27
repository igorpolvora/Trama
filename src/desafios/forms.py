from django import forms

from .models import Desafio, ParticipacaoDesafio


class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ["nome", "descricao", "regras"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "regras": forms.Textarea(attrs={"rows": 5}),
        }


class ParticipacaoDesafioForm(forms.ModelForm):
    class Meta:
        model = ParticipacaoDesafio
        fields = []
