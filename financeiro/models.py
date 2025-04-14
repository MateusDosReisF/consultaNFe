# financeiro/models.py
from django.db import models
from django.utils import timezone

class ContaPagar(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)

    def marcar_como_paga(self):
        self.pago = True
        self.data_pagamento = timezone.now()
        self.save()

    def __str__(self):
        return f"Conta a Pagar: {self.descricao} - Valor: {self.valor} - Pago: {self.pago}"

class ContaReceber(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    recebido = models.BooleanField(default=False)
    data_recebimento = models.DateField(null=True, blank=True)

    def marcar_como_recebido(self):
        self.recebido = True
        self.data_recebimento = timezone.now()
        self.save()

    def __str__(self):
        return f"Conta a Receber: {self.descricao} - Valor: {self.valor} - Recebido: {self.recebido}"
