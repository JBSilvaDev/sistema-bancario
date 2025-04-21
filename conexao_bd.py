import sqlite3 as bd

def conectar_bd():
  con = bd.connect('./contas.db')
  return con

def login(agencia:str,cont_numero:int, senha:str = None):
  con = conectar_bd()
  querys = con.cursor()

  try:
    if senha==None:
      querys.execute('SELECT * FROM contas WHERE id = ? AND agencia = ?', (cont_numero, agencia))
      conta = querys.fetchone()
      print(f'O valor sera depositado na conta de {conta[2]}')
    else:
      print(f'Acessando conta {cont_numero}...')
      querys.execute('SELECT * FROM contas WHERE id = ? AND senha = ? AND agencia = ?', (cont_numero, senha, agencia))
      conta = querys.fetchone()
      if conta is None:
        print('Conta inexistente ou senha incorreta.')
        return 
      print(f'Bem-vindo(a) {conta[2]}!')

  except:
    return False

  con.commit()
  querys.close()
  con.close()
  return conta