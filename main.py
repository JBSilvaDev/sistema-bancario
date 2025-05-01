from criar_contas import criar_conta
from depositar import deposito
from sacar import saque
from extrato import extrato_conta

if __name__ == '__main__':
  # criar_conta('Joaquim', 'senha123', 958.16)
  # deposito(1, 70)
  # extrato_conta('0001', 1, senha='1')
  # saque(agencia='0001', cont_numero=1, senha='1', valor_saque=20)
  
  loop = True
  while loop:
    print('''
    1 - Criar conta
    2 - Depositar
    3 - Sacar
    4 - Extrato
    5 - Sair
    ''')
    
    opcao = input('Escolha uma opção: ')
    
    if opcao == '1':
      nome = input('Digite seu nome: ')
      senha = input('Digite sua senha: ')
      nascimento = input('Digite sua data de nascimento (DD/MM/AAAA): ')
      cpf = input('Digite seu CPF (apenas números): ')
      cidade = input('Digite sua cidade: ')
      estado = input('Digite seu estado (UF): ')
      bairro = input('Digite seu bairro: ', )
      rua_numero = input('Digite o nome da rua e o número: ')
      endereco = f"{rua_numero}, {bairro} - {cidade}/{estado}"
      criar_conta (nome, senha, nascimento, cpf, endereco)
    
    elif opcao == '2':
      agencia = input('Digite o número da agência: ')
      cont_numero = int(input('Digite o número da conta: '))
      deposito_valor = float(input('Digite o valor a depositar: '))
      deposito(agencia, cont_numero, deposito_valor)
    
    elif opcao == '3':
      agencia = input('Digite o número da agência: ')
      cont_numero = int(input('Digite o número da conta: '))
      senha = input('Digite sua senha: ')
      saque_valor = float(input('Digite o valor a sacar: '))
      saque(agencia=agencia, cont_numero=cont_numero, senha=senha, valor_saque=saque_valor)
    
    elif opcao == '4':
      agencia = input('Digite o número da agência: ')
      cont_numero = int(input('Digite o número da conta: '))
      senha = input('Digite sua senha: ')
      extrato_conta(agencia, cont_numero, senha=senha)
    
    elif opcao == '5':
      loop = False
    
    else:
      print('Opção inválida. Tente novamente.')