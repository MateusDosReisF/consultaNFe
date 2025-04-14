# forms.py
from django import forms
from .models import Empresa,Etiqueta,NotaFiscal

class ConfiguracaoEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['razao_social','cnpj', 'senha_certificado', 'local_certificado', 'status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['local_certificado'].widget = forms.ClearableFileInput(attrs={'multiple': False})


class ConfiguracaoEtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields=['cor','descricao']
