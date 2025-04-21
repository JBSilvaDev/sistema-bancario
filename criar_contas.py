from conexao_bd import conectar_bd
from datetime import datetime
import utils as convert

def criar_conta (nome, senha, nascimento, cpf, endereco, saldo_inicial=0):

  con = conectar_bd()
  querys = con.cursor()
  
  querys.execute('''CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    agencia TEXT DEFAULT "0001",
    nome TEXT NOT NULL, 
    senha TEXT NOT NULL,
    saldo REAL NOT NULL,
    saques_dia INTEGER DEFAULT 0,
    data_nascimento TEXT DEFAULT NULL,
    cpf TEXT UNIQUE,
    endereco TEXT DEFAULT NULL,
    historico TEXT DEFAULT NULL
  )''')

  print('Criando conta...')

  try:
    querys.execute('''
                INSERT INTO contas (nome,  senha, saldo, saques_dia,data_nascimento, cpf, endereco, historico)
                VALUES (?, ?, ?,?,?,?,?,?)
                ''', (nome, senha, saldo_inicial, 0, nascimento, cpf, endereco, f"[{convert.mapa_para_str({'Criação de conta':convert.date_para_iso()})}]")
                )
  except Exception as e:
    if 'UNIQUE constraint failed' in str(e):
      print('CPF já cadastrado.')
      return
    else:
      print('Erro ao criar conta:', e)
      return
  
  conta_id = querys.lastrowid

  querys.execute('SELECT * FROM contas WHERE id = ?', (conta_id,))
  conta = querys.fetchone()
  print(f'Conta criada com sucesso!, agencia: 0001, conta: {conta[0]}')
  
  con.commit()
  querys.close()
  con.close()