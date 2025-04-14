# financeiro/urls.py
from django.urls import path
from .views import (
    listar_contas_pagar,
    listar_contas_receber,
    adicionar_conta_pagar,
    adicionar_conta_receber,
    marcar_pago,
    marcar_recebido,
)

urlpatterns = [
    path('contas-pagar/', listar_contas_pagar, name='listar_contas_pagar'),
    path('contas-receber/', listar_contas_receber, name='listar_contas_receber'),
    path('contas-pagar/adicionar/', adicionar_conta_pagar, name='adicionar_conta_pagar'),
    path('contas-receber/adicionar/', adicionar_conta_receber, name='adicionar_conta_receber'),
    path('contas-pagar/<int:conta_id>/marcar_pago/', marcar_pago, name='marcar_pago'),
    path('contas-receber/<int:conta_id>/marcar_recebido/', marcar_recebido, name='marcar_recebido'),
]
