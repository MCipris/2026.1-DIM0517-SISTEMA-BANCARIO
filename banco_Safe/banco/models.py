from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Conta(models.Model):

    TIPO_SIMPLES = "SIMPLES"
    TIPO_BONUS = "BONUS"
    TIPO_POUPANCA = "POUPANCA"

    TIPOS_CONTA = (
        (TIPO_SIMPLES, "Conta Simples"),
        (TIPO_BONUS, "Conta Bônus"),
        (TIPO_POUPANCA, "Conta Poupança"),
    )

    usuario = models.CharField(
        max_length=20
    )

    numero = models.CharField(
        max_length=20,
        unique=True
    )

    saldo = models.FloatField(
        default=0
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_CONTA,
        default=TIPO_SIMPLES
    )

    pontuacao = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.numero} - {self.tipo}"