from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Conta

class ContaService:
    
    @staticmethod
    def cadastrar_conta(usuario, numero: str, tipo: str = Conta.TIPO_SIMPLES) -> Conta:
        if Conta.objects.filter(numero=numero).exists():
            raise ValueError("Uma conta com este número já existe.")

        pontuacao_inicial = 10 if tipo == Conta.TIPO_BONUS else 0

        conta = Conta.objects.create(
            usuario=usuario,
            numero=numero,
            tipo=tipo,
            pontuacao=pontuacao_inicial,
            saldo=saldo_inicial
        )

        return conta

    @staticmethod
    def consultar_saldo(numero: str) -> Decimal:
        try:
            conta = Conta.objects.get(numero=numero)
            return conta.saldo
        except ObjectDoesNotExist:
            raise ValueError("Conta não encontrada.")
        
    @staticmethod
    def creditar(numero: str, valor: Decimal) -> Conta:

        conta = ContaService._get_conta(numero)

        conta.saldo += valor

        if conta.tipo == Conta.TIPO_BONUS:

            pontos = int(valor // 100)

            conta.pontuacao += pontos

        conta.save()

        return conta
    
@staticmethod
    def debitar(numero: str, valor: Decimal) -> 'Conta':
        if valor <= 0:
            raise ValueError("O valor de débito deve ser positivo.")
        
        conta = Conta.objects.get(numero=numero)
        
        if conta.tipo_conta in [TipoConta.SIMPLES, TipoConta.BONUS]:
            if (conta.saldo - valor) < Decimal('-1000.00'):
                raise ValueError("Operação negada. O limite de saldo negativo (R$ -1000,00) seria ultrapassado.")
        elif conta.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar o débito.")
        
        conta.saldo -= valor 
        conta.save()
        return conta
    
@staticmethod
    def transferir(numero_origem: str, numero_destino: str, valor: Decimal):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if numero_origem == numero_destino:
            raise ValueError("Conta de origem e destino não podem ser iguais.")

        with transaction.atomic():
            conta_origem = Conta.objects.get(numero=numero_origem)
            conta_destino = Conta.objects.get(numero=numero_destino)
            
            if conta_origem.tipo_conta in [TipoConta.SIMPLES, TipoConta.BONUS]:
                if (conta_origem.saldo - valor) < Decimal('-1000.00'):
                    raise ValueError("Operação negada. O limite de saldo negativo (R$ -1000,00) seria ultrapassado na conta de origem.")
            elif conta_origem.saldo < valor:
                raise ValueError("Saldo insuficiente na conta de origem.")

        if origem.saldo < valor:
            raise ValueError("Saldo insuficiente.")

        origem.saldo -= valor
        destino.saldo += valor

        if destino.tipo == Conta.TIPO_BONUS:

            pontos = int(valor // 150)

            destino.pontuacao += pontos

        origem.save()
        destino.save()

        return origem, destino
    
    @staticmethod
    def render_juros(taxa_percentual: Decimal):
        contas_poupanca = Conta.objects.filter(
            tipo=Conta.TIPO_POUPANCA
        )

        for conta in contas_poupanca:

            rendimento = conta.saldo * (taxa_percentual / 100)

            conta.saldo += rendimento

            conta.save()
