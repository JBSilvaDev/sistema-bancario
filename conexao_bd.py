import sqlite3 as bd

def conectar_bd():
  con = bd.connect('./contas.db')
  return con

def login(cont_numero:int, senha:str = None):
  con = conectar_bd()
  querys = con.cursor()

  try:
    if senha==None:
      querys.execute('SELECT * FROM contas WHERE id = ?', (cont_numero, ))
      conta = querys.fetchone()
      print(f'O valor sera depositado na conta de {conta[1]}')
    else:
      print(f'Acessando conta {cont_numero}...')
      querys.execute('SELECT * FROM contas WHERE id = ? AND senha = ?', (cont_numero, senha, ))
      conta = querys.fetchone()
      print(f'Bem-vindo(a) {conta[1]}!')

    if conta is None:
      print('Conta inexistente.')
      return 
    
  except:
    print('Erro ao acessar o banco de dados.')
    return False

  con.commit()
  querys.close()
  con.close()
  return conta