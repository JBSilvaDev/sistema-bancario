import sqlite3 as bd

def conectar_bd():
  print('Conectando ao banco de dados...')
  con = bd.connect('./contas.db')
  return con