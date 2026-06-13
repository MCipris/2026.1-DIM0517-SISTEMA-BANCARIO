from decimal import Decimal
from django.db import transaction
from .models import Conta

class ContaService:
    
    @staticmethod
    def _get_conta(numero: str) -> Conta:
        try:
            return Conta.objects.get(numero=numero)
        except Conta.DoesNotExist:
            raise ValueError("Conta não encontrada.")

    @staticmethod
    def cadastrar_conta(usuario, numero: str, tipo: str = Conta.TIPO_SIMPLES) -> Conta:
        if Conta.objects.filter(numero=numero).exists():
            raise ValueError("Uma conta com este número já existe.")
        
        if tipo not in [Conta.TIPO_SIMPLES, Conta.TIPO_BONUS, Conta.TIPO_POUPANCA,]:
            raise ValueError("Tipo de conta inválido.")

        if tipo == Conta.TIPO_BONUS:
            pontuacao_inicial = 10
        else:
            pontuacao_inicial = 0

        conta = Conta.objects.create(
                usuario=usuario,
                numero=numero,
                tipo=tipo,
                pontuacao=pontuacao_inicial)

        return conta

    @staticmethod
    def consultar_saldo(numero: str) -> Decimal:
        conta = ContaService._get_conta(numero)
        return conta.saldo
        
    @staticmethod
    def creditar(numero: str, valor: Decimal) -> Conta:
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        conta = ContaService._get_conta(numero)

        conta.saldo += valor

        if conta.tipo == Conta.TIPO_BONUS:

            pontos = int(valor // Decimal("100"))

            conta.pontuacao += pontos

        conta.save()

        return conta
    
    @staticmethod
    def debitar(numero: str, valor: Decimal) -> 'Conta':
        if valor <= 0:
            raise ValueError("O valor de débito deve ser positivo.")
        
        conta = ContaService._get_conta(numero)
        
        if conta.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar o débito.")
        
        conta.saldo -= valor 
        conta.save()
        return conta
    
    @staticmethod
    @transaction.atomic
    def transferir(numero_origem: str, numero_destino: str, valor: Decimal):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if numero_origem == numero_destino:
            raise ValueError("Conta de origem e destino não podem ser iguais.")

        conta_origem = ContaService._get_conta(numero_origem)
        conta_destino = ContaService._get_conta(numero_destino)
        
        if conta_origem.saldo < valor:
            raise ValueError("Saldo insuficiente na conta de origem.")

        conta_origem.saldo -= valor
        conta_destino.saldo += valor

        if conta_destino.tipo == Conta.TIPO_BONUS:

            pontos = int(valor // Decimal("200"))

            conta_destino.pontuacao += pontos

        conta_origem.save()
        conta_destino.save()    

        return conta_origem, conta_destino
    
    @staticmethod
    def render_juros(taxa_percentual: Decimal):
        contas_poupanca = Conta.objects.filter(
            tipo=Conta.TIPO_POUPANCA
        )

        if taxa_percentual <= 0:
            raise ValueError("Taxa de juros inválida.")

        for conta in contas_poupanca:

            rendimento = conta.saldo * (taxa_percentual / Decimal("100"))

            conta.saldo += rendimento

            conta.save()