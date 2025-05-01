
class Controle:
  def __init__(self, dicionario:dict={}):
    self.dicionario = {k: v for k, v in dicionario.items()}



  @property
  def valida_cliente(self):

    if not self.dicionario:
      return ValueError("Nenhum dado foi passado.")
    
    if not 'nome' in self.dicionario.keys():
      return ValueError("Nome cliente não informado.")
    
    if not 'senha' in self.dicionario.keys():
      return ValueError("Senha cliente não informada.")
    
    if not 'saldo' in self.dicionario.keys():
      self.dicionario['saldo'] = 0
    
    if not 'data_nascimento' in self.dicionario.keys():
      return ValueError("Data nascimento cliente não informada.")
    
    if not 'cpf' in self.dicionario.keys():
      return ValueError("CPF cliente não informado.")
    
    if not 'endereco' in self.dicionario.keys():
      return ValueError("Endereço cliente não informado.")
    
    return True
  






    
  
  