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
            pontuacao=pontuacao_inicial
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
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        conta = ContaService._get_conta(numero)

        conta.saldo += valor

        if conta.tipo == Conta.TIPO_BONUS:

            pontos = int(valor // 100)

            conta.pontuacao += pontos

        conta.save()

        return conta
    
    @staticmethod
    def debitar(numero: str, valor: Decimal) -> Conta:
        if valor <= 0:
            raise ValueError("Valor inválido.")

        conta = ContaService._get_conta(numero)

        if conta.saldo < valor:
            raise ValueError("Saldo insuficiente.")

        conta.saldo -= valor

        conta.save()

        return conta
    
    @staticmethod
    @transaction.atomic
    def transferir(origem_num: str, destino_num: str, valor: Decimal):
        if valor <= 0:
            raise ValueError("Valor inválido.")

        origem = ContaService._get_conta(origem_num)
        destino = ContaService._get_conta(destino_num)

        if origem.saldo < valor:
            raise ValueError("Saldo insuficiente.")

        origem.saldo -= valor
        destino.saldo += valor

        if destino.tipo == Conta.TIPO_BONUS:

            pontos = int(valor // 200)

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