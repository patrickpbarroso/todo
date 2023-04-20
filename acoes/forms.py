from django import forms

from .models import Acao

class AcaoForm(forms.ModelForm):

    class Meta:
        model = Acao
        fields = ('codigo', 'descricao', 'open', 'closed', 'high', 'low', 'volume')