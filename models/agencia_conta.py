from abc import ABC, abstractmethod
from data.conexao_bd import DadosBanco
from view.cliente import Cliente
from controller.banco_controler import Controle
from utils.utilidades import Utils


UTILS = Utils()

class Agencia(ABC):
    def __init__(self, agNumero):
        self.agNumero = agNumero


    @abstractmethod
    def conectar_bd(self):
        pass


class Conta(Agencia):
    
    def __init__(self, agNumero, cliente:Cliente):
        super().__init__(agNumero)
        self.cliente = cliente
        self.criar_conta()

    @property
    def conectar_bd(self):
        banco = DadosBanco()
        return banco.conectar_bd()

    def criar_conta(self, saldo_inicial=0):
        dict_conta = self.cliente.__dict__
        con = self.conectar_bd
        query = con.cursor()

        validacao_cliente = self.cliente.validacao_cliente()

        if not validacao_cliente:
           print(validacao_cliente)

        # print(utils)


        if validacao_cliente == True:
            print("*"*50)
            try:
              historico = f"[{self.utils.mapa_para_str({'Criação de conta': UTILS.date_para_iso()})}]"
              query.execute(
                    """
                    INSERT INTO contas 
                    (nome, senha, saldo, saques_dia, data_nascimento, cpf, endereco, historico)
                    VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        dict_conta['nome'],
                        dict_conta['senha'],
                        saldo_inicial,
                        0,  # saques_dia
                        dict_conta['nascimento'],
                        dict_conta['cpf'],
                        dict_conta['endereco'],
                        historico
                    )
                )
            except Exception as e:
              
              if 'UNIQUE constraint failed' in str(e):
                print('CPF já cadastrado.')
                return
              else:
                print('Erro ao criar conta:', e)
                return
              
            ultimo_id = query.lastrowid

            query.execute(
               '''
               SELECT * FROM contas 
               WHERE id = ?
               ''', (ultimo_id)
               )

            conta = UTILS.tupla_para_dicionario(query.fetchone())

            print(f'Conta criada com sucesso!, agencia: {conta["agencia"]}, conta: {conta['id']}')
            
            self.login(conta['cpf'], conta['senha'])

            con.commit()
            query.close()
            con.close()
            


    def login(self, cpf:str, senha:str):
        con = self.conectar_bd
        query = con.cursor()

        try:
            query.execute('''
                        SELECT * FROM contas
                        WHERE cpf = ? AND senha = ?
                        ''', 
                        (cpf, senha)
                        )
            
            conta = UTILS.tupla_para_dicionario(query.fetchone())
            if not conta is None:
                print(f'Bem-vindo(a) {conta["nome"]}!')
                return conta
            else:
                print('Conta inexistente ou senha incorreta.')
                return None
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            return None
        finally:
            query.close()
            con.close()