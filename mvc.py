from multiprocessing import parent_process
from pydoc import cli
from models.agencia_conta import Conta
from models.cliente import Cliente
from data.conexao_bd import DadosBanco
from models.agencia_conta import Conta
from models.cliente import Cliente

from view.visualizacao import user_interface, conta_cliente,deposito, saque


# cliente = Cliente('Lucas', '30/05/1991', 'Rua A, 123',cpf='00', senha='00')
cliente = Cliente(cpf='00', senha='00')
conta = Conta()
auth = conta.login(cliente)
# conta.criar_conta()
# conta = Conta()
# conta.depositar('0001', 2, 587.15)
# conta.sacar(valor_saque=100, conta_auth=conta_auth)
# user_interface()
# deposito(auth=auth)
saque(auth=auth)


