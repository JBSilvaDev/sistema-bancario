import json
from datetime import datetime
import pandas as pd

class Utils:
  
  @staticmethod
  def data_para_iso():
    return datetime.now().isoformat()


  @staticmethod
  def texto_json( texto):
    return json.loads(texto)

  @staticmethod
  def mapa_para_str( mapa):
      # a= None
      # for k, v in mapa.items():
      #     a = {k: v.isoformat()}
      return json.dumps(mapa)


  @staticmethod
  def str_para_mapa( texto):
      a = json.loads(texto)
      for i in a:
          for k, v in i.items():
            i[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y %H:%M:%S")
      df = pd.DataFrame(a)
      df = df.melt(var_name="Evento", value_name="Data/Hora")
      df = df.dropna()
      return df

  @staticmethod
  def filtro_extrato( df, evento):
      # Verifica se contem a palavra na coluna evento
      filtro = df['Evento'].str.contains(evento)
      # Retorna apenas itens que atendem a condição
      return df[filtro]

  @staticmethod
  def compara_datas( data1):
      b = datetime.strptime(data1, "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
      a = datetime.today().strftime("%d/%m/%Y")
      return a==b
  
  @staticmethod
  def dicionario_para_str( dicionario):
    # a= None
    # for k, v in dicionario.items():
    #     a = {k: v.isoformat()}
    return json.dumps(dicionario)


  @staticmethod
  def str_para_dicionario( texto):
      a = json.loads(texto)
      for i in a:
          for k, v in i.items():
            i[k] = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y %H:%M:%S")
      df = pd.DataFrame(a)
      df = df.melt(var_name="Evento", value_name="Data/Hora")
      df = df.dropna()
      return df
  
  @staticmethod
  def tupla_para_dicionario(tupla):
     chaves = [
    "id", "agencia", "nome", "senha", "saldo", "saques_dia", 
    "data_nascimento", "cpf", "endereco", "historico"
]
     dicionario = dict(zip(chaves, tupla))
     print(dicionario)
     return dicionario
  