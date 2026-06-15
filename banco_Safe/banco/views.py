from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import ContaService
from .models import Conta
from .serializers import ContaSerializer

class ContaCreateView(APIView):

    def post(self, request):

        conta = ContaService.cadastrar_conta(
            usuario_conta=request.data["usuario"],
            numero_conta=request.data["numero"],
            tipo_conta=request.data.get(
                "tipo",
                Conta.TIPO_SIMPLES
            )
        )

        serializer = ContaSerializer(conta)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ContaDetailView(APIView):
    def get(self, request, numero_conta):

        conta = ContaService._get_conta(numero_conta)

        serializer = ContaSerializer(conta)

        return Response(serializer.data)

class SaldoView(APIView):
    def get(self, request, numero_conta):

        conta = ContaService._get_conta(numero_conta)

        return Response({
            "saldo": conta.saldo
        })

class ContaCreditoView(APIView):

    def put(self, request, numero_conta):

        conta = Conta.objects.get(numero=numero_conta)

        conta = ContaService.creditar(
            conta.numero,
            float(request.data["valor"])
        )

        serializer = ContaSerializer(conta)

        return Response(serializer.data)
    
class ContaDebitoView(APIView):

    def put(self, request, numero_conta):

        conta = Conta.objects.get(numero=numero_conta)

        conta = ContaService.debitar(
            conta.numero,
            float(request.data["valor"])
        )

        serializer = ContaSerializer(conta)

        return Response(serializer.data)
    
class TransferenciaView(APIView):
    def put(self, request):

        ContaService.transferir(
            request.data["from"],
            request.data["to"],
            float(request.data["amount"])
        )

        return Response({
            "message": "Transferência realizada com sucesso."
        })
    
class ContaRendimentoView(APIView):

    def put(self, request):

        taxa = float(
            request.data["taxa"]
        )

        ContaService.render_juros(taxa)

        return Response({
            "mensagem": "Rendimento aplicado."
        })