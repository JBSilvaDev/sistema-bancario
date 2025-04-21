from conexao_bd import conectar_bd, login
from datetime import datetime, timedelta
import utils
import json

def saque (cont_numero:int, senha, valor_saque:float):

  con = conectar_bd()
  querys = con.cursor()

  
  try:
    conta = login(cont_numero, senha)
    
    # Verifica o saldo da conta
    if conta[3] < valor_saque or valor_saque <= 0:
      print('Saldo insuficiente. ou valor de saque inválido.')
      return
    if conta[4] >= 5:
      historico_saques = utils.str_para_mapa(conta[5])
      saques = utils.filtro_extrato(historico_saques, 'Saque')
      if (utils.compara_datas(saques['Data/Hora'].to_list()[-1])):
        print('Limite de saques diários atingido.')
        return
      else:
        querys.execute(f'''
                 UPDATE contas SET saques_dia = 0 WHERE id = {cont_numero}
                 ''')
        
    historico = json.loads(conta[5])
    historico.append({f'Saque - {valor_saque:.2f}': utils.date_para_iso()})
    novo_historico = utils.mapa_para_str(historico)

    querys.execute('''
            UPDATE contas SET historico = ? WHERE id = ?
        ''', (novo_historico, cont_numero))

    
    querys.execute('''
                 UPDATE contas SET saldo = saldo - ?, saques_dia = saques_dia + 1 WHERE id = ?
                 ''', (valor_saque, cont_numero))
    
    
    
    print(f'Saque de R$ {valor_saque:.2f} realizado com sucesso!')
    print(f'Saldo atual: R$ {conta[3] - valor_saque:.2f}')
  except:
    print('Erro ao acessar o banco de dados.')
    return
  
  con.commit()
  querys.close()
  con.close()