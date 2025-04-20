from conexao_bd import conectar_bd, login

def extrato_conta (cont_numero:int, senha):

  con = conectar_bd()
  querys = con.cursor()

  
  try:
    conta = login(cont_numero, senha)
    print(f'Saldo atual: R$ {conta[3]:.2f}')

  except:
    print('Erro ao acessar o banco de dados.')
    return
  
  con.commit()
  querys.close()
  con.close()