from models.agencia_conta import Conta
from view.cliente import Cliente

# cliente = Cliente('Lucas', '30/05/1991', 'Rua A, 123',cpf='12345678900', senha='123456')
cliente = Cliente(cpf='12345678900', senha='123456')
conta = Conta(cliente)
# conta.criar_conta()
conta_auth = conta.login(cliente=cliente)
# conta.depositar('0001', 1, 587.15, conta_auth=conta_auth)
conta.sacar(valor_saque=100, conta_auth=conta_auth)



