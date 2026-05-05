from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Conta(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="conta"
    )

    numero = models.CharField(max_length=20, unique=True)

    saldo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    def __str__(self):
        return f"{self.usuario.username} - Conta {self.numero}"