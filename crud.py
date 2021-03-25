"""
Autor: Rafael Martins
E-mail: rafagha@gmail.com
Data: 23/03/2021

Objetivo: Um CRUD simples para exercitar oque estou estudando,
o programa cadastra clientes, exibe, atualiza e delete os mesmos.
"""

# parte 1 - importando os modulos necessarios

# importando os modulos
# importando o banco de dados
import sqlite3

# para deixar as tabelas bonitas, essa lib é nota 10!
from prettytable import from_db_cursor

# esse modulo me permite verificar se o banco de dados ja foi criado
# não é nem necessario, mas resolvi usar so para dar um toque
# diferencial no meu script
import os.path

# modulo para sair do programa
import sys

# fim da parte 1


#parte 2 - banco de dados

# aqui ele verifica se o banco de dados existe
# se não existir ele cria
if not os.path.exists("clientes.db"):

    # conectando e criando(caso nao exista) o banco de dados
    conn = sqlite3.connect("clientes.db")

    # definindo o nosso cursor
    cursor = conn.cursor()

    # aqui vem a criação da tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf VARCHAR(11) NOT NULL,
        fone TEXT
    );
    """)

    print("Tabela criada com sucesso.")

else:
    # conectando e criando(caso nao exista) o banco de dados
    # sempre tem que conectar para poder funcionar
    conn = sqlite3.connect("clientes.db")

    # definindo o nosso cursor
    cursor = conn.cursor()

# fim parte 2


# parte 3 - funções do programa
def func_verifica_cadastro():
    """ Essa função verifica se o cliente ja existe no banco de dados
        Primeiro a função pede que seja digitado o CPF, depois ele olha se o CPF
        existe dentro do banco de dados(linha 81).
        Se não existir dai ele chama a função que adiciona o novo cliente
        ao banco de dados.
    """

    cpf = input("Informe o CPF do usuario: ")

    cursor.execute("""
    SELECT cpf FROM clientes WHERE cpf = ?;
    """,([cpf]))


    if cursor.fetchone() == None:
        func_inserir_novo_cadastro(cpf)
        input()
        func_menu()

    else:
        print("Cliente ja possui cadastro")
        input() # input vazio é so para dar um charme
        func_menu()


def func_inserir_novo_cadastro(cpf):
    """
        Essa é a função que de fato adiciona o usuario ao banco de dados.
    """
    nome = input("Informe o nome do cliente: ")
    fone = input("Informe o numero do cliente: ")

    cursor.execute("""
    INSERT INTO clientes (nome, cpf, fone)
    VALUES (?,?,?) """, (nome, cpf, fone))
    conn.commit()

    conn.close()
    print(f"Cliente {nome} cadastrado com sucesso!")


def func_exibir_registros():
    """Essa função exibe os cadastros"""

    # conectando e criando(caso nao exista) o banco de dados
    conn = sqlite3.connect("clientes.db")

    # definindo o nosso cursor
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM clientes;
    """)
    tabela = from_db_cursor(cursor) # Essa lib é linda e monta a tabela
    print(tabela)
    input()

    func_menu() # sempre que uma rotina chega ao fim eu chamo o menu de novo


def func_editar_registro():
    """função responsavel pela edição/update dos clientes"""

    cursor.execute("""
        SELECT * FROM clientes;
    """)

    tabela = from_db_cursor(cursor)
    print(tabela)

    id = input("Informe o ID desejado: ")
    cursor.execute("""
    SELECT * From clientes WHERE id = ?;
    """, ([id]))

    if len(list(cursor)) > 0: # aqui ele verifica se a consulta do banco de dados encontrou o cliente buscado
        novo_nome = input("Informe o novo nome: ")
        cpf_novo = input("Informe o CPF: ")
        fone_novo = input("Informe o novo numero: ")

        cursor.execute("""
        UPDATE clientes SET nome = ?, cpf = ?, fone = ? WHERE id = ?
        """, (novo_nome, cpf_novo, fone_novo, id))

        conn.commit()
        conn.close()

        print("Dados Atualizados com sucesso")
        input()
        func_menu()

    else:
        print("ID não encontrado\nEsse ID esta correto?")
        func_editar_registro()




def func_deletar_registro():
    """Aqui ele deleta um usuario através do seu ID"""

    cursor.execute("""
        SELECT * FROM clientes;
    """)
    tabela = from_db_cursor(cursor)
    print(tabela)

    id = input("Informe o ID desejado: ")

    cursor.execute("""
       SELECT * From clientes WHERE id = ?;
       """, ([id]))

    if len(list(cursor)) > 0: #verifica se cliente existe

        cursor.execute("""
            DELETE From clientes WHERE id = ?;
            """, ([id]))

        conn.commit()
        conn.close()

        print("Cliente deletado com sucesso")
        func_menu()

    else:
        print("ID nao encontrado na lista")
        func_deletar_registro()

def func_sair():
    """Aqui ele encerra o programa"""

    print("Encerrando programa.")
    try:
        conn.close()
    except:
        pass
    else:
        sys.exit()

def func_menu():
    """Menu principal"""

    print()
    print("="*10,"Menu","="*10)
    print("-"*26)
    pauzinho = "|"
    print(f"| 1 - Adicionar Cliente {pauzinho:>2}") # Create
    print(f"| 2 - Exibir Clientes   {pauzinho:>2}") # Read
    print(f"| 3 - Atualizar Cliente {pauzinho:>2}") # Update
    print(f"| 4 - Deletar Cliente   {pauzinho:>2}") # Delete
    print(f"| 5 - Sair do Programa  {pauzinho:>2}")
    print("-"*26)

    n = input("\nInforme a opção desejada: ")

    if n == "1":
        func_verifica_cadastro()

    elif n == "2":
        func_exibir_registros()

    elif n == "3":
        func_editar_registro()

    elif n == "4":
        func_deletar_registro()

    elif n == "5":
        func_sair()

    else:
        print("Opção Invalida")
        input()
        func_menu()


func_menu()
