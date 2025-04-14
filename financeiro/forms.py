# financeiro/forms.py
from django import forms
from .models import ContaPagar, ContaReceber

class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = ['descricao', 'valor', 'data_vencimento']

class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['descricao', 'valor', 'data_vencimento']
