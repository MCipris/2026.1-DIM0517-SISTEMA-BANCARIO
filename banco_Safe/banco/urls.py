from django.urls import path

from .views import (
    ContaCreateView,
    ContaDetailView,
    SaldoView,
    ContaCreditoView,
    ContaDebitoView,
    TransferenciaView,
    ContaRendimentoView
)

urlpatterns = [
    path("conta/", ContaCreateView.as_view()),
    path("conta/<str:numero>", ContaDetailView.as_view()),
    path("conta/<str:numero>/saldo", SaldoView.as_view()),
    path("conta/<str:numero>/credito", ContaCreditoView.as_view()),
    path("conta/<str:numero>/debito", ContaDebitoView.as_view()),
    path("conta/transferencia", TransferenciaView.as_view()),
    path("conta/rendimento", ContaRendimentoView.as_view()),
]