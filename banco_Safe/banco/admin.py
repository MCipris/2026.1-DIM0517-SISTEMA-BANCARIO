from django.contrib import admin
from .models import Conta

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ("numero", "saldo")
    search_fields = ("numero",)