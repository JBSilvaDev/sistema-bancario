from conexao_bd import conectar_bd

def criar_conta (nome, login, senha, saldo_inicial=0):

  con = conectar_bd()
  querys = con.cursor()
  
  querys.execute('''CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    login TEXT NOT NULL, 
    senha TEXT NOT NULL,
    saldo REAL NOT NULL
  )''')

  print('Criando conta...')
  querys.execute('''
                  INSERT INTO contas (nome, login, senha, saldo)
                  VALUES (?, ?, ?, ?)
                  ''', (nome, login, senha, saldo_inicial))
  

  querys.execute('SELECT * FROM contas WHERE login = ? AND senha = ?', (login, senha))
  conta = querys.fetchone()
  print('Conta criada com sucesso!, seu código de conta é: ', conta[0])
  
  con.commit()
  querys.close()
  con.close()
  

criar_conta('Guilhermes', 'guilherme', '12356', 0)