from data.conexao_bd import DadosBanco
from controller.banco_controler import Controle

class Cliente:
  def __init__(self,nome, senha, nascimento, cpf, endereco):
    self.nome = nome
    self.senha = senha
    self.nascimento = nascimento
    self.cpf = cpf
    self.endereco = endereco

  def validacao_cliente(self):
    dict_conta = {
        "nome": self.nome,
        "senha": self.senha,
        "data_nascimento": self.nascimento,
        "cpf": self.cpf,
        "endereco": self.endereco,
    }
    controle = Controle(dict_conta)
    validacao = controle.valida_cliente
    return validacao