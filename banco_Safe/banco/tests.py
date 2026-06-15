from django.test import TestCase
from .services import ContaService
from .models import Conta


class bancoTest(TestCase):
    def setUp(self):
        self.conta_simples = ContaService.cadastrar_conta("Usuario1", "1", Conta.TIPO_SIMPLES, 10.00)
        self.conta_bonus = ContaService.cadastrar_conta("Usuario2", "2", Conta.TIPO_BONUS)
        self.conta_poupanca = ContaService.cadastrar_conta("Usuario3", "3", Conta.TIPO_POUPANCA)


    def test_cadastro_simples(self):
        self.conta_teste = ContaService.cadastrar_conta("Usuario", "5", Conta.TIPO_SIMPLES, 10.00)
        
        with self.assertRaises(ValueError):
            ContaService.cadastrar_conta("Usuario2", "5", Conta.TIPO_SIMPLES)
        
        self.assertEqual(self.conta_teste.usuario, "Usuario")
        self.assertEqual(self.conta_teste.numero, "5")
        self.assertEqual(self.conta_teste.tipo, Conta.TIPO_SIMPLES)
        self.assertEqual(self.conta_teste.pontuacao, 0)
        self.assertEqual(self.conta_teste.saldo, 10.00)


    def test_cadastro_bonus(self):
        self.conta_teste = ContaService.cadastrar_conta("Usuario", "5", Conta.TIPO_BONUS)
        
        with self.assertRaises(ValueError):
            ContaService.cadastrar_conta("Usuario2", "5", Conta.TIPO_BONUS)
        
        self.assertEqual(self.conta_teste.usuario, "Usuario")
        self.assertEqual(self.conta_teste.numero, "5")
        self.assertEqual(self.conta_teste.tipo, Conta.TIPO_BONUS)
        self.assertEqual(self.conta_teste.pontuacao, 10)


    def test_cadastro_poupanca(self):
        self.conta_teste = ContaService.cadastrar_conta("Usuario", "5", Conta.TIPO_POUPANCA)
        
        with self.assertRaises(ValueError):
            ContaService.cadastrar_conta("Usuario2", "5", Conta.TIPO_POUPANCA)
        
        self.assertEqual(self.conta_teste.usuario, "Usuario")
        self.assertEqual(self.conta_teste.numero, "5")
        self.assertEqual(self.conta_teste.tipo, Conta.TIPO_POUPANCA)
        self.assertEqual(self.conta_teste.pontuacao, 0)
    

    def test_consultar_simples(self):
        self.valores = {"numero":"1", "tipo":Conta.TIPO_SIMPLES, "saldo": 10, "pontuacao":0}
        self.assertEqual(ContaService.consultar_conta(self.conta_simples.numero), self.valores)
    

    def test_consultar_bonus(self):
        self.valores = {"numero":"1", "tipo":Conta.TIPO_SIMPLES, "saldo": 0, "pontuacao":0}
        self.assertEqual(ContaService.consultar_conta(self.conta_simples.numero), self.valores)


    def test_consultar_poupanca(self):
        self.valores = {"numero":"1", "tipo":Conta.TIPO_SIMPLES, "saldo": 0, "pontuacao":0}
        self.assertEqual(ContaService.consultar_conta(self.conta_simples.numero), self.valores)


    def test_consultar_saldo(self):
        self.conta_simples.saldo = 100.00
        self.conta_simples.save()
        self.assertEqual(ContaService.consultar_saldo(self.conta_simples.numero), 100.00)

        self.conta_bonus.saldo = 100.00
        self.conta_bonus.save()
        self.assertEqual(ContaService.consultar_saldo(self.conta_bonus.numero), 100.00)

        self.conta_poupanca.saldo = 100.00
        self.conta_poupanca.save()
        self.assertEqual(ContaService.consultar_saldo(self.conta_poupanca.numero), 100.00)
    

    def test_creditar(self):
        with self.assertRaises(ValueError):
            ContaService.creditar(self.conta_poupanca.numero, -100.0)
        with self.assertRaises(ValueError):
            ContaService.creditar(self.conta_bonus.numero, -100.0)
        with self.assertRaises(ValueError):
            ContaService.creditar(self.conta_simples.numero, -100.0)
        
        ContaService.creditar(self.conta_poupanca.numero, 100.0)
        ContaService.creditar(self.conta_simples.numero, 100.0)
        ContaService.creditar(self.conta_bonus.numero, 100.0)

        self.assertEqual(self.conta_poupanca.saldo, 100.0)
        self.assertEqual(self.conta_simples.saldo, 110.0)
        self.assertEqual(self.conta_bonus.saldo, 100.0)
        self.assertEqual(self.conta_bonus.pontuacao, 1)


    def test_debitar(self):
        self.conta_simples.saldo = 100.00
        self.conta_bonus.saldo = 100.0
        self.conta_poupanca.saldo = 100.0

        self.conta_simples.save()
        self.conta_bonus.save()
        self.conta_poupanca.save()

        with self.assertRaises(ValueError):
            ContaService.debitar(self.conta_simples.numero, -10)
        with self.assertRaises(ValueError):
            ContaService.debitar(self.conta_bonus.numero, -10)
        with self.assertRaises(ValueError):
            ContaService.debitar(self.conta_poupanca.numero, -10)
        
        with self.assertRaises(ValueError):
            ContaService.debitar(self.conta_simples.numero, 200)
        with self.assertRaises(ValueError):
            ContaService.debitar(self.conta_bonus.numero, 200)
        with self.assertRaises(ValueError):
            ContaService.debitar(self.conta_poupanca.numero, 200)
        
        ContaService.debitar(self.conta_simples.numero, 50)
        self.assertEqual(self.conta_simples.saldo, 50)
        ContaService.debitar(self.conta_bonus.numero, 50)
        self.assertEqual(self.conta_bonus.saldo, 50)
        ContaService.debitar(self.conta_poupanca.numero, 50)
        self.assertEqual(self.conta_poupanca.saldo, 50)
    

    def test_tranferencia(self):
        self.conta_simples2 = ContaService.cadastrar_conta("Usuario11", "11", Conta.TIPO_SIMPLES)
        self.conta_bonus2 = ContaService.cadastrar_conta("Usuario12", "12", Conta.TIPO_BONUS)
        self.conta_poupanca2 = ContaService.cadastrar_conta("Usuario13", "13", Conta.TIPO_POUPANCA)

        self.conta_simples.saldo = 200.00
        self.conta_bonus.saldo = 200.0
        self.conta_poupanca.saldo = 200.0
        self.conta_simples.save()
        self.conta_bonus.save()
        self.conta_poupanca.save()

        self.conta_simples2.saldo = 200.00
        self.conta_bonus2.saldo = 200.0
        self.conta_poupanca2.saldo = 200.0
        self.conta_simples2.save()
        self.conta_bonus2.save()
        self.conta_poupanca2.save()

        with self.assertRaises(ValueError):
            ContaService.transferir(self.conta_simples.numero, self.conta_simples2.numero, -10)
        with self.assertRaises(ValueError):
            ContaService.transferir(self.conta_bonus.numero, self.conta_bonus2.numero, -10)
        with self.assertRaises(ValueError):
            ContaService.transferir(self.conta_poupanca.numero, self.conta_poupanca2.numero, -10)
        
        with self.assertRaises(ValueError):
            ContaService.transferir(self.conta_simples.numero, self.conta_simples2.numero, 300)
        with self.assertRaises(ValueError):
            ContaService.transferir(self.conta_bonus.numero, self.conta_bonus2.numero, 300)
        with self.assertRaises(ValueError):
            ContaService.transferir(self.conta_poupanca.numero, self.conta_poupanca2.numero, 300)

        ContaService.transferir(self.conta_simples.numero, self.conta_simples2.numero, 100)
        self.assertEqual(self.conta_simples.saldo, 100)
        self.assertEqual(self.conta_simples2.saldo, 100)
        ContaService.transferir(self.conta_poupanca.numero, self.conta_poupanca2.numero, 100)
        self.assertEqual(self.conta_poupanca.saldo, 100)
        self.assertEqual(self.conta_poupanca2.saldo, 100)
        ContaService.transferir(self.conta_bonus.numero, self.conta_bonus2.numero, 100)
        self.assertEqual(self.conta_bonus.saldo, 100)
        self.assertEqual(self.conta_bonus2.saldo, 100)
        self.assertEqual(self.conta_bonus2.pontuacao, 1)

    
    def test_juros(self):
        self.conta_poupanca2 = ContaService.cadastrar_conta("Usuario13", "13", Conta.TIPO_POUPANCA)
       
        self.conta_poupanca.saldo = 100
        self.conta_poupanca2.saldo = 200

        self.conta_poupanca.save()
        self.conta_poupanca.save()
        
        ContaService.render_juros(2)
        self.assertEqual(self.conta_poupanca.saldo, 102)
        self.assertEqual(self.conta_poupanca2.saldo, 204)