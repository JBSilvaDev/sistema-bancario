from conexao_bd import conectar_bd, login

def saque (cont_numero:int, senha, valor_saque:float):

  con = conectar_bd()
  querys = con.cursor()

  
  try:
    conta = login(cont_numero, senha)
    
    # Verifica o saldo da conta
    if conta[3] < valor_saque or valor_saque <= 0:
      print('Saldo insuficiente. ou valor de saque inválido.')
      return
    
    querys.execute('''
                 UPDATE contas SET saldo = saldo - ? WHERE id = ?
                 ''', (valor_saque, cont_numero))
    print(f'Saque de R$ {valor_saque:.2f} realizado com sucesso!')
    print(f'Saldo atual: R$ {conta[3] - valor_saque:.2f}')
  except:
    print('Erro ao acessar o banco de dados.')
    return
  
  con.commit()
  querys.close()
  con.close()