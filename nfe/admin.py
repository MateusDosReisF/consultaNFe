from django.contrib import admin
from .models import NotaFiscal, Etiqueta,Empresa


class EmpresaAdminForm(admin.ModelAdmin):
   list_display = ('razao_social','cnpj','senha_certificado','local_certificado','status')
   search_fields = ('razao_social','cnpj','senha_certificado','local_certificado','status')
admin.site.register(Empresa,EmpresaAdminForm)


class NotaFiscalAdminForm(admin.ModelAdmin):
      list_display = ('numero','nf','data','status_nfe','emissor','emissor_cnpj','chaveNfe')
      search_fields = ('numero','nf','data','status_nfe','emissor','emissor_cnpj','chaveNfe')
admin.site.register(NotaFiscal,NotaFiscalAdminForm)

class EtiquetaAdminForm(admin.ModelAdmin):
      list_display = ('cor','descricao')
      search_fields = ('cor','descricao')
admin.site.register(Etiqueta,EtiquetaAdminForm)