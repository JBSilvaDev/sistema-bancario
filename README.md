# Sistema Bancário

Este é um projeto de um sistema bancário simples desenvolvido em Python, utilizando SQLite como banco de dados. O sistema permite criar contas, realizar depósitos, saques e consultar extratos.

## Funcionalidades

- **Criar Conta**: Criação de contas com nome, login, senha e saldo inicial.
- **Depositar**: Realizar depósitos em contas existentes.
- **Sacar**: Realizar saques de contas existentes, com validação de senha.
- **Consultar Extrato**: Exibir o saldo e o histórico de transações de uma conta.

## Estrutura do Projeto

- `main.py`: Arquivo principal que executa o menu interativo do sistema.
- `conexao_bd.py`: Gerencia a conexão com o banco de dados SQLite.
- `criar_contas.py`: Contém a lógica para criação de contas.
- `depositar.py`: Contém a lógica para realizar depósitos.
- `sacar.py`: Contém a lógica para realizar saques.
- `extrato.py`: Contém a lógica para consultar o extrato de uma conta.

## Requisitos

- Python 3.8 ou superior
- Biblioteca SQLite (já incluída no Python)

## Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-bancario.git
   cd sistema-bancario
   ```

2. Execute o arquivo `main.py`:
   ```bash
   python main.py
   ```
3. Siga as instruções no menu para interagir com o sistema.

### Exemplo de Uso
> Criar Conta
- Escolha a opção 1 - **Criar conta** no menu.
- Insira o nome, senha e saldo inicial.
- O sistema exibirá o ID da conta criada.
> Depositar
- Escolha a opção 2 - **Depositar** no menu.
- Insira o número da conta e o valor do depósito.
- O sistema confirmará o depósito.
> Sacar
- Escolha a opção 3 - **Sacar** no menu.
- Insira o número da conta, a senha e o valor do saque.
- O sistema confirmará o saque ou exibirá uma mensagem de erro.
> Consultar Extrato
- Escolha a opção 4 - **Extrato** no menu.
- Insira o número da conta e senha.
- O sistema exibirá o saldo e o histórico de transações.

### Estrutura do Banco de Dados
> Tabela `contas`:
- `id` (INTEGER): Identificador único da conta.
- `agencia` (TEXT): Número da agência, padrão "0001".
- `nome` (TEXT): Nome do titular da conta.
- `senha` (TEXT): Senha da conta.
- `saldo` (REAL): Saldo inicial da conta.
- `saques_dia` (INTEGER): Contador de saques diários.
- `data_nascimento` (TEXT): Data de nascimento do titular da conta.
- `cpf` (TEXT): CPF do titular da conta.
- `endereco` (TEXT): Endereço do titular da conta.
- `historico` (TEXT): Histórico de transações da conta.
