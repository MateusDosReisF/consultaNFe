# financeiro/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContaPagar, ContaReceber
from .forms import ContaPagarForm, ContaReceberForm

def listar_contas_pagar(request):
    contas = ContaPagar.objects.all()
    return render(request, 'listar_contas_pagar.html', {'contas': contas})

def listar_contas_receber(request):
    contas = ContaReceber.objects.all()
    return render(request, 'listar_contas_receber.html', {'contas': contas})

def adicionar_conta_pagar(request):
    if request.method == "POST":
        form = ContaPagarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_contas_pagar')
    else:
        form = ContaPagarForm()
    return render(request, 'adicionar_conta_pagar.html', {'form': form})

def adicionar_conta_receber(request):
    if request.method == "POST":
        form = ContaReceberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_contas_receber')
    else:
        form = ContaReceberForm()
    return render(request, 'adicionar_conta_receber.html', {'form': form})

def marcar_pago(request, conta_id):
    conta = get_object_or_404(ContaPagar, id=conta_id)
    conta.marcar_como_paga()
    return redirect('listar_contas_pagar')

def marcar_recebido(request, conta_id):
    conta = get_object_or_404(ContaReceber, id=conta_id)
    conta.marcar_como_recebido()
    return redirect('listar_contas_receber')
