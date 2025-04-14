from django.db import models

class Empresa(models.Model):
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    senha_certificado = models.CharField(max_length=50)
    local_certificado = models.FileField(upload_to='uploads/')
    status = models.BooleanField(default=True)

class Etiqueta(models.Model):
    cor=models.CharField(max_length=30)
    descricao=models.CharField(max_length=100)

    def __str__(self):
        return f"Etiqueta {self.descricao}"
        

class NotaFiscal(models.Model):
    numero = models.CharField(max_length=20)
    nf= models.CharField(max_length=100)
    data = models.CharField(max_length=100)
    status_nfe= models.CharField(max_length=100)
    emissor = models.CharField(max_length=100)
    emissor_cnpj=models.CharField(max_length=20)
    destinatario =models.CharField(max_length=100)
    destinatario_cnpj=models.CharField(max_length=20)
    valor_total = models.CharField(max_length=20)
    xml = models.TextField()
    etiqueta = models.ForeignKey(Etiqueta,on_delete=models.CASCADE,related_name='etiqueta_NotaFiscal',blank=True,null=True)
    chaveNfe=models.CharField(max_length=100)

    def __str__(self):
        return f"Nota Fiscal {self.numero}"

