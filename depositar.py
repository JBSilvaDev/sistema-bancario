from conexao_bd import conectar_bd, login
import utils
import json

def deposito (cont_numero:int, deposito):

  con = conectar_bd()
  querys = con.cursor()

  
  try:
    conta = login(cont_numero)

    if deposito <= 0:
      print('Valor de depósito inválido.')
      return
    querys.execute('''
                 UPDATE contas SET saldo = saldo + ? WHERE id = ?
                 ''', (deposito, cont_numero))
  
    historico = json.loads(conta[5])
    historico.append({f'Depósito - {deposito:.2f}': utils.date_para_iso()})
    novo_historico = utils.mapa_para_str(historico)
    querys.execute('''
            UPDATE contas SET historico = ? WHERE id = ?
        ''', (novo_historico, cont_numero))

    print(f'Depósito de R$ {deposito:.2f} realizado com sucesso!')

  except:
    print('Erro ao acessar o banco de dados.')
    return
  
  con.commit()
  querys.close()
  con.close()