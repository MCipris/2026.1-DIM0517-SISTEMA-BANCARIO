import json
from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import ContaService

@csrf_exempt
def cadastrar_conta_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        numero = data.get('numero')
        tipo_conta = data.get('tipo', 'SIMPLES').upper()
        saldo_inicial_str = data.get('saldo_inicial')
        
        try:
            if tipo_conta == 'POUPANCA' and saldo_inicial_str is None:
                raise ValueError("É obrigatório informar o saldo_inicial para criar uma Conta Poupança.")
            
            saldo_inicial = Decimal(saldo_inicial_str) if saldo_inicial_str is not None else Decimal('0.00')
            
            ContaService.cadastrar_conta(numero, tipo_conta, saldo_inicial)
            return JsonResponse({"mensagem": f"Conta {tipo_conta} cadastrada com sucesso."}, status=201)
        except (ValueError, InvalidOperation) as e:
            return JsonResponse({"erro": str(e)}, status=400)
