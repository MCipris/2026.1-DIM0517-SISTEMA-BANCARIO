from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Conta
from django.db.models import F

class ContaService:
    
    @staticmethod
    def cadastrar_conta(numero: str) -> Conta:
        if Conta.objects.filter(numero=numero).exists():
            raise ValueError("Uma conta com este número já existe.")
        # Cria a conta com saldo zero por padrão (definido no Model)
        return Conta.objects.create(numero=numero)

    @staticmethod
    def consultar_saldo(numero: str) -> Decimal:
        try:
            conta = Conta.objects.get(numero=numero)
            return conta.saldo
        except ObjectDoesNotExist:
            raise ValueError("Conta não encontrada.")
        
    @staticmethod
    def creditar(numero: str, valor: Decimal) -> Conta:
        if valor <= 0:
            raise ValueError("O valor a ser creditado deve ser maior que zero.")
        
        conta = Conta.objects.get(numero=numero)
        conta.saldo = F('saldo') + valor
        conta.save()
        return conta
    
    @staticmethod
    def debitar(numero: str, valor: Decimal) -> Conta:
        if valor <= 0:
            raise ValueError("O valor a ser debitado deve ser maior que zero.")
        
        conta = Conta.objects.get(numero=numero)
        
        conta.saldo = F('saldo') - valor
        conta.save()
        return conta
    
    @staticmethod
    @transaction.atomic
    def transferir(origem_num: str, destino_num: str, valor: Decimal):
        if valor <= 0:
            raise ValueError("Valor inválido.")

        origem = ContaService._get_conta(origem_num)
        destino = ContaService._get_conta(destino_num)

        origem.saldo = F('saldo') - valor
        destino.saldo = F('saldo') + valor

        origem.save()
        destino.save()

        origem.refresh_from_db()
        destino.refresh_from_db()

        return origem, destino