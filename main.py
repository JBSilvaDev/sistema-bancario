from encodings.punycode import T
from criar_contas import criar_conta
from depositar import deposito
from sacar import saque
from extrato import extrato_conta

if __name__ == '__main__':
  # extrato_conta(1, 'senha123')
  # deposito(1, 1000)
  # saque(1, 'senha123', 900)
  # criar_conta('Joaquim', 'senha123', 958.16)
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
      saldo_inicial = float(input('Digite o valor do saldo inicial: '))
      criar_conta(nome, senha, saldo_inicial)
    
    elif opcao == '2':
      cont_numero = int(input('Digite o número da conta: '))
      deposito_valor = float(input('Digite o valor a depositar: '))
      deposito(cont_numero, deposito_valor)
    
    elif opcao == '3':
      cont_numero = int(input('Digite o número da conta: '))
      senha = input('Digite sua senha: ')
      saque_valor = float(input('Digite o valor a sacar: '))
      saque(cont_numero, senha, saque_valor)
    
    elif opcao == '4':
      cont_numero = int(input('Digite o número da conta: '))
      senha = input('Digite sua senha: ')
      extrato_conta(cont_numero, senha)
    
    elif opcao == '5':
      loop = False
    
    else:
      print('Opção inválida. Tente novamente.')