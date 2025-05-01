from abc import ABC, abstractmethod
from calendar import c
from data.conexao_bd import DadosBanco
from view.cliente import Cliente
from controller.banco_controler import Controle
from utils.utilidades import Utils


UTILS = Utils()

class Agencia(ABC):
    def __init__(self, agNumero='0001'):
        self.agNumero = agNumero


    @abstractmethod
    def conectar_bd(self):
        pass


class Conta(Agencia):
    
    def __init__(self, cliente:Cliente):
        super().__init__()
        self.cliente = cliente
        


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
           pass

        if validacao_cliente == True:
            try:
              historico = f"[{UTILS.mapa_para_str({'Criação de conta': UTILS.data_para_iso()})}]"
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
                        0,
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
               f'''
               SELECT * FROM contas
               WHERE id = {ultimo_id}
               AND agencia = "{self.agNumero}"
               '''
               )

            conta = UTILS.tupla_para_dicionario(query.fetchone())
            print(f'Conta criada com sucesso!, agencia: {conta["agencia"]}, conta: {conta['id']}')
            

            con.commit()
            query.close()
            con.close()
            self.login(Cliente(cpf=conta['cpf'], senha=conta['senha']))
            


    def login(self, cliente:Cliente=None, e_reload=False):
        cpf = cliente.cpf
        senha = cliente.senha
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
                if not e_reload:
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

    def depositar(self, agencia, conta_numero, valor_deposito, /, *,cliente:Cliente=None):
        conta_auth = None
        con = self.conectar_bd
        query = con.cursor()

        try:
            conta_auth = self.login(cliente)
        except:
            print('Depósito sem autenticação...')

        try:  
            query.execute(
                    '''
                    SELECT historico FROM contas WHERE id = ? AND agencia = ?
                    ''',
                    (conta_numero, agencia)
                    )
            historico = UTILS.texto_json(query.fetchone()[0])
            if conta_auth is None:
                if valor_deposito <= 0:
                    print('Valor de depósito inválido.')
                    return ValueError('Valor de depósito inválido.')
                historico.append(
                    {f'Depósito - {valor_deposito:.2f}': UTILS.data_para_iso()}
                    )
                novo_historico = UTILS.mapa_para_str(historico)

                query.execute(
                    '''
                    UPDATE contas SET 
                    saldo = saldo + ?,
                    historico = ?
                    WHERE id = ? AND agencia = ?
                    ''',
                    (valor_deposito, novo_historico, conta_numero, agencia,)
                )
                con.commit()
                print(f'Depósito de R$ {valor_deposito:.2f} realizado com sucesso!')

            elif conta_auth:
                print('=*='*10) 
                if valor_deposito <= 0:
                    print('Valor de depósito inválido.')
                    return ValueError('Valor de depósito inválido.')
                historico.append(
                    {f'Depósito - {valor_deposito:.2f}': UTILS.data_para_iso()}
                    )
                novo_historico = UTILS.mapa_para_str(historico)

                query.execute(
                    '''
                    UPDATE contas SET 
                    saldo = saldo + ?,
                    historico = ?
                    WHERE id = ? AND agencia = ?
                    ''',
                    (valor_deposito, novo_historico, conta_numero, agencia,)
                )
                con.commit()
                print(f'Depósito de R$ {valor_deposito:.2f} realizado com sucesso!')

                recarrega_conta = self.login(cliente, True)
                print(f"Saldo atual: R$ {recarrega_conta['saldo']:.2f}")
                return recarrega_conta
                
        except Exception as e:
            print(f'Erro ao depositar: {e}')
        finally:
            query.close()
            con.close()
