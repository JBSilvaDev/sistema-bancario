from conexao_bd import conectar_bd

def criar_conta (nome, login, senha, saldo_inicial=0):

  con = conectar_bd()
  querys = con.cursor()
  
  querys.execute('''CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    login TEXT NOT NULL, 
    senha TEXT NOT NULL
  )''')

  querys.execute('''
                  INSERT INTO contas (nome, login, senha, saldo)
                  VALUES (?, ?, ?, ?)
                  ''', (nome, login, senha, saldo_inicial))
  
  con.commit()
  querys.close()
  con.close()
  