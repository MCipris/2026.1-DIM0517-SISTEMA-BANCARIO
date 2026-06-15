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
    def cadastrar_conta(usuario_conta: str, numero_conta: str, tipo_conta: str = Conta.TIPO_SIMPLES, saldo_conta: float = 0) -> Conta:
        if Conta.objects.filter(numero=numero_conta).exists():
            raise ValueError("Uma conta com este número já existe.")
        
        if tipo_conta not in [Conta.TIPO_SIMPLES, Conta.TIPO_BONUS, Conta.TIPO_POUPANCA,]:
            raise ValueError("Tipo de conta inválido.")

        if tipo_conta == Conta.TIPO_SIMPLES and saldo_conta < -1000.00:
            raise ValueError("Criação de conta inválida.")

        if tipo_conta == Conta.TIPO_BONUS:
            pontuacao_inicial = 10
        else:
            pontuacao_inicial = 0

        if tipo_conta == Conta.TIPO_SIMPLES:
            conta = Conta.objects.create(
                    usuario=usuario_conta,
                    numero=numero_conta,
                    saldo=saldo_conta,
                    tipo=tipo_conta,
                    pontuacao=pontuacao_inicial)
        else:
            conta = Conta.objects.create(
                    usuario=usuario_conta,
                    numero=numero_conta,
                    tipo=tipo_conta,
                    pontuacao=pontuacao_inicial)

        return conta

    @staticmethod
    def consultar_saldo(numero: str) -> float:
        conta = ContaService._get_conta(numero)
        return conta.saldo
        
    @staticmethod
    def consultar_conta(numero: str) -> dict:
        conta = ContaService._get_conta(numero)

        return {
            "numero": conta.numero,
            "tipo": conta.tipo,
            "saldo": conta.saldo,
            "pontuacao": conta.pontuacao
        }
    
    @staticmethod
    def creditar(numero: str, valor: float) -> Conta:
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
    def debitar(numero: str, valor: float) -> Conta:
        if valor <= 0:
            raise ValueError("O valor de débito deve ser positivo.")
        
        conta = ContaService._get_conta(numero)
        
        if conta.tipo in [Conta.TIPO_SIMPLES, Conta.TIPO_BONUS]:
            if (conta.saldo - valor) < -1000.00:
                raise ValueError("Operação negada. O limite de saldo negativo (R$ -1000,00) seria ultrapassado.")
        elif conta.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar o débito.")
        
        conta.saldo -= valor 
        conta.save()
        return conta
    
    @staticmethod
    @transaction.atomic
    def transferir(numero_origem: str, numero_destino: str, valor: float):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if numero_origem == numero_destino:
            raise ValueError("Conta de origem e destino não podem ser iguais.")

        conta_origem = ContaService._get_conta(numero_origem)
        conta_destino = ContaService._get_conta(numero_destino)
        
        if conta_origem.tipo in [Conta.TIPO_SIMPLES, Conta.TIPO_BONUS]:
            if (conta_origem.saldo - valor) < -1000.00:
                raise ValueError("Operação negada. O limite de saldo negativo (R$ -1000,00) seria ultrapassado na conta de origem.")
        elif conta_origem.saldo < valor:
            raise ValueError("Saldo insuficiente na conta de origem.")

        conta_origem.saldo -= valor
        conta_destino.saldo += valor

        if conta_destino.tipo == Conta.TIPO_BONUS:

            pontos = int(valor // 150)

            conta_destino.pontuacao += pontos


        conta_origem.save()
        conta_destino.save()    

        return conta_origem, conta_destino
    
    @staticmethod
    def render_juros(taxa_percentual: float):
        contas_poupanca = Conta.objects.filter(
            tipo=Conta.TIPO_POUPANCA
        )

        if taxa_percentual <= 0:
            raise ValueError("Taxa de juros inválida.")

        for conta in contas_poupanca:

            rendimento = conta.saldo * (taxa_percentual / 100)

            conta.saldo += rendimento

            conta.save()