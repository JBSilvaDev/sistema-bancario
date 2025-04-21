from conexao_bd import conectar_bd, login
import utils

def extrato_conta (cont_numero:int, senha):

  con = conectar_bd()
  querys = con.cursor()

  
  try:
    conta = login(cont_numero, senha)
    print("="*50)
    print(f'Saldo atual: R$ {conta[3]:.2f}')
    print("="*50)

    historico = utils.str_para_mapa(conta[5])
    print(historico)
    print("="*50)

  except:
    print('Erro ao acessar o banco de dados.')
    return
  
  con.commit()
  querys.close()
  con.close()