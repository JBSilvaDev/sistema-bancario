from conexao_bd import conectar_bd

def criar_conta (nome, senha, saldo_inicial=0):

  con = conectar_bd()
  querys = con.cursor()
  
  querys.execute('''CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    senha TEXT NOT NULL,
    saldo REAL NOT NULL
  )''')

  print('Criando conta...')
  querys.execute('''
                  INSERT INTO contas (nome,  senha, saldo)
                  VALUES (?, ?, ?)
                  ''', (nome, senha, saldo_inicial))
  
  conta_id = querys.lastrowid

  querys.execute('SELECT * FROM contas WHERE id = ?', (conta_id,))
  conta = querys.fetchone()
  print('Conta criada com sucesso!, seu código de conta é: ', conta[0])
  
  con.commit()
  querys.close()
  con.close()
  