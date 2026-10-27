from django import forms

from .models import Comentario, Conteudo


class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ["tipo", "titulo", "texto", "visibilidade"]
        widgets = {
            "texto": forms.Textarea(attrs={"rows": 6}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(attrs={"rows": 4}),
        }
