from conexao_bd import conectar_bd

def deposito (cont_numero, deposito):

  con = conectar_bd()
  querys = con.cursor()

  
  try:
    print(f'Acessando conta {cont_numero}...')
    querys.execute('SELECT * FROM contas WHERE id = ?', (cont_numero,))
    conta = querys.fetchone()

    if conta is None:
      print('Conta inexistente.')
      return
    
    if deposito <= 0:
      print('Valor de depósito inválido.')
      return
    
    querys.execute('''
                 UPDATE contas SET saldo = saldo + ? WHERE id = ?
                 ''', (deposito, cont_numero))
  except:
    print('Erro ao acessar o banco de dados.')
    return
  
  con.commit()
  querys.close()
  con.close()