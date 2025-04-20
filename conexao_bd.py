import sqlite3 as bd

def conectar_bd():
  con = bd.connect('./contas.db')
  return con

def login(cont_numero:int, senha:str):
  con = conectar_bd()
  querys = con.cursor()

  try:
    print(f'Acessando conta {cont_numero}...')
    querys.execute('SELECT * FROM contas WHERE id = ? AND senha = ?', (cont_numero, senha, ))
    conta = querys.fetchone()

    if conta is None:
      print('Conta inexistente.')
      return 

    print(f'Bem-vindo(a) {conta[1]}!')
    
  except:
    print('Erro ao acessar o banco de dados.')
    return False

  con.commit()
  querys.close()
  con.close()
  return conta