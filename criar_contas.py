from conexao_bd import conectar_bd
from datetime import datetime
import utils as convert

def criar_conta (nome, senha, saldo_inicial=0):

  con = conectar_bd()
  querys = con.cursor()
  
  querys.execute('''CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    senha TEXT NOT NULL,
    saldo REAL NOT NULL,
    saques_dia INTEGER DEFAULT 0,
    historico TEXT DEFAULT NULL
  )''')

  print('Criando conta...')

  querys.execute('''
                  INSERT INTO contas (nome,  senha, saldo, saques_dia, historico)
                  VALUES (?, ?, ?,?,?)
                  ''', (nome, senha, saldo_inicial, 0, f"[{convert.mapa_para_str({'Criação de conta':convert.date_para_iso()})}]")
                  )
  
  conta_id = querys.lastrowid

  querys.execute('SELECT * FROM contas WHERE id = ?', (conta_id,))
  conta = querys.fetchone()
  print('Conta criada com sucesso!, seu código de conta é: ', conta[0])
  
  con.commit()
  querys.close()
  con.close()