from abc import ABC, abstractmethod
from calendar import c
from http import client
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

    def depositar(self, agencia, conta_numero, valor_deposito, /, *,cliente:Cliente=None, conta_auth=None):
        # conta_auth = None
        con = self.conectar_bd
        query = con.cursor()

        try:
            conta_auth = self.login(cliente, True)
        except:
            pass

        if cliente==None:
            try:
                cliente = Cliente(cpf=conta_auth['cpf'], senha=conta_auth['senha'])
            except:
                print('Autenticação atual falhou, refaça o login.')

        try:  
            query.execute(
                    '''
                    SELECT historico FROM contas WHERE id = ? AND agencia = ?
                    ''',
                    (conta_numero, agencia)
                    )
            historico = UTILS.texto_json(query.fetchone()[0])
            if conta_auth is None:
                print('Depósito sem autenticação...')
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
                conta_auth = recarrega_conta
                print(f"Saldo atual: R$ {recarrega_conta['saldo']:.2f}")
                return conta_auth
                
        except Exception as e:
            print(f'Erro ao depositar: {e}')
        finally:
            query.close()
            con.close()

    def sacar(self, cliente:Cliente=None, conta_auth=None, valor_saque=0):
        con = self.conectar_bd
        query = con.cursor()

        print('===='*10)
        print("Validando infomações de saque...")
        print('===='*10)
        try:
            conta_auth = self.login(cliente, True)
        except:
            pass

        if cliente==None:
            try:
                cliente = Cliente(cpf=conta_auth['cpf'], senha=conta_auth['senha'])
            except:
                print('Autenticação atual falhou, refaça o login.')     

        if conta_auth is None:
            print("Conta não autenticada. Faça login primeiro.")
        elif valor_saque <= 0:
            print("Valor de saque inválido. Digite um valor válido.")
        elif conta_auth['saldo'] < valor_saque:
            print("Saldo insuficiente para este saque.")
        else:
            print('===='*10)
            print("Autenticação realizada com sucesso!")
            print("Efetuando saque solicitado...")
            print('===='*10)
            # Obtem historico para determinar limite de saques diarios
            historico = UTILS.str_para_mapa(conta_auth['historico'])
            historico_saques = UTILS.filtro_extrato(historico, 'Depósito')
            # Verifica se a conta atingiu o limite de saques diários
            if conta_auth['saques_dia'] >= 5:
                # Se limite tiver atingido, verifica se a ultima data de saque é hoje
                if UTILS.compara_datas(historico_saques['Data/Hora'].to_list()[-1]):
                    print('Limite de saques diários atingido.')
                    return
                # Se o limite for atingido e a data for diferente de hoje, recomeça a contagem
                else:
                    query.execute(
                        '''
                        UPDATE contas SET saques_dia = 0 WHERE id = ? AND agencia = ?
                        ''',
                        (conta_auth['id'], conta_auth['agencia'])
                        )
                    con.commit()
            
            print('=*='*10)
            # Realiza o saque subtraindo o valor solicitado do saldo no bd
            query.execute('''
                 UPDATE contas SET saldo = saldo - ?, saques_dia = saques_dia + 1 WHERE id = ? AND agencia = ?
                 ''', (valor_saque, conta_auth['id'], conta_auth['agencia']))
            con.commit()
            print(f'Saque de R$ {valor_saque:.2f} realizado com sucesso!')

            

            # Obtem historico de saques e adicona o saque realizado ao extrato
            historico_dict = UTILS.texto_json(conta_auth['historico'])
            historico_dict.append({f'Saque - {valor_saque:.2f}': UTILS.data_para_iso()})
            att_historico = UTILS.mapa_para_str(historico_dict)

            query.execute('''
                UPDATE contas SET historico = ? WHERE id = ? AND agencia = ?
                ''', 
                (att_historico, conta_auth['id'], conta_auth['agencia']))
            
            recarrega_conta = self.login(cliente, True)
            conta_auth = recarrega_conta
            print(f'Saldo atual: R$ {conta_auth["saldo"]:.2f}')

            con.commit()
            query.close()
            con.close()
            return conta_auth

        
