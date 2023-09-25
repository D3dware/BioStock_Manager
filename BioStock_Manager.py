import time
import sqlite3
import os
import sys

############################################################################################
#                           CLASSES:
############################################################################################


class Substancia:
    def __init__(self, nome, quantidade):
        self.nome = nome
        self.quantidade = quantidade


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(self, query, values=None):
        if values:
            self.cursor.execute(query, values)

        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def obter_todos_os_dados(self):
        try:
            query = "SELECT * FROM estoque"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            dados_formatados = [f"{linha[1]}, {linha[2]}, {linha[3]}" for linha in result]
            return dados_formatados

        except Exception as error:
            print(f"ERRO: Falha ao obter todos os dados ->  {error}\n")
            return []

    def verificar_substancia(self, substancia, quantidade):
        self.cursor.execute("SELECT substancia AND quantidade FROM estoque WHERE substancia = ? AND quantidade = ?", (substancia, quantidade,))
        return self.cursor.fetchone() is not None

    def adicionar_substancia(self, substancia, quantidade):
        try:
            if not self.verificar_substancia(substancia, quantidade):
                self.cursor.execute("""
                INSERT INTO estoque (substancia, quantidade)
                VALUES (?, ?)
                """, (substancia, quantidade))
                self.connection.commit()
                print("\n[ Substância Adicionada com Sucesso ]\n")

            else:
                print("\nERRO: Substância já Existe no Banco de Dados.\n")

        except Exception as error:
            print(f"ERRO: Falha ao Adicionar Substância -> {error}")

    def deletar_todas_substancias(self):
        try:
            query = "DELETE FROM estoque"
            self.execute(query)
            print("-> Todas as Substâncias foram Deletadas do Banco de Dados.\n")
            print("_______________________________________________________________________________\n")

        except Exception as error:
            print(f"ERRO: Falha ao Limpar Banco de Dados -> {error}\n")
            print("_______________________________________________________________________________\n")


class GerenciadorStock:
    def __init__(self, db):
        self.db = db

    def adicionar_substancia(self, substancia, quantidade):
        try:
            verificar = self.db.verificar_substancia(substancia, quantidade)
            if not verificar:
                query = "INSERT INTO estoque (substancia, quantidade) VALUES (?, ?)"
                values = (substancia, quantidade)
                self.db.execute(query, values)
                print(f"-> Substância {substancia}-{quantidade} Adicionada com Sucesso.\n")
            else:
                print(f"-> Substância {substancia}-{quantidade} já Existe no Banco de Dados. Ignorando Duplicata.\n")

        except Exception as error:
            print(f"ERRO: Falha ao Adicionar Substância -> {error}\n")

    def listar_substancias(self):
        query = "SELECT * FROM estoque"
        substancias = self.db.fetch_all(query)
        for sub in substancias:
            print("              ---------------------------------              \n")
            print(f"¬ ID: {sub[0]}\n¬ SUBSTÂNCIA: {sub[1]}\n¬ QUANTIDADE (mL ou g): {sub[2]}\n")

    def pesquisar_substancia(self, substancia):
        if substancia:
            query = f"SELECT * FROM estoque WHERE substancia = '{substancia}'"
            substancias = self.db.fetch_all(query)
            for sub in substancias:
                print("              ---------------------------------              \n")
                print(f"¬ ID: {sub[0]}\n¬ SUBSTÂNCIA: {sub[1]}\n¬ QUANTIDADE (mL ou g): {sub[2]}\n")

        else:
            print("ERRO: Dados Informados Incorretamente ! Tente Novamente.\n")

    def atualizar_quantidade(self, id_substancia, quantidade):
        query = "UPDATE estoque SET quantidade = ? WHERE id = ?"
        values = (quantidade, id_substancia)
        self.db.execute(query, values)
        print(f"-> Quantidade da Substância com ID {id_substancia} Atualizada com Sucesso.\n")

    def deletar_substancia(self, id_substancia):
        query = "DELETE FROM estoque WHERE id = ?"
        self.db.execute(query, (id_substancia,))
        print(f"\n-> Substância com ID {id_substancia} Deletada com Sucesso.\n")


###########################################################################################


db = Database("BioStock.db")

gerenciador = GerenciadorStock(db)


def database():
    db = Database("BioStock.db")
    db.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY,
            substancia TEXT,
            quantidade REAL
            )""")


def limpar_tela():
    try:
        os.system("cls" if os.name == "nt" else "clear")

    except Exception as e:
        print(f"{e}\n")


def volar_menu():
    choic = input("VOLTAR ao menu principal?\nDIGITE [1]¬ Sim: ")
    match choic:
        case "1":
            limpar_tela()
            menu_principal(db)
        case _:
            limpar_tela()
            menu_principal(db)


def opcoes_principal(db):
    try:
        opcao = input("[*] DIGITE o número da Opção [ENTER para confirmar]: ")

        match opcao:
            case "1":
                try:
                    limpar_tela()
                    print("_______________________________________________________________________________\n")
                    print("[*] PREENCHA os dados a seguir para cadastrar a Substância:\n")
                    subs = input("¬ NOME DA SUBSTÂNCIA: ").title()
                    quant = float(input("¬ QUANTIDADE (mL ou g): "))
                    print("_______________________________________________________________________________\n")
                    gerenciador.adicionar_substancia(subs, quant)
                    time.sleep(3)
                    limpar_tela()
                    menu_principal(db)

                except Exception as error:
                    print(f"ERRO: Não foi possível adicionar a Substância! -> {error}\n")
                    time.sleep(3)
                    menu_principal(db)

                except KeyboardInterrupt:
                    print("[*] Operação cancelada pelo usuário.\n")
                    time.sleep(3)
                    limpar_tela()
                    menu_principal(db)

            case "2":
                try:
                    limpar_tela()
                    print("_______________________________________________________________________________\n")
                    info = input("¬ NOME DA SUBSTÂNCIA: ").title()
                    print("_______________________________________________________________________________\n")
                    gerenciador.pesquisar_substancia(info)
                    volar_menu()

                except Exception as error:
                    print(f"ERRO: Falha ao pesquisar Substância! -> {error}, Tente Novamente...\n")
                    time.sleep(4)
                    opcoes_principal(db)

            case "3":
                try:
                    limpar_tela()
                    print("_______________________________________________________________________________\n")
                    gerenciador.listar_substancias()
                    print("_______________________________________________________________________________\n")
                    volar_menu()

                except Exception as error:
                    print(f"ERRO: {error}\n")
                    time.sleep(5)
                    opcoes_principal(db)

            case "4":
                try:
                    limpar_tela()
                    print("_______________________________________________________________________________\n")
                    id = input("¬ ID da Substância: ")
                    quant = float(input("¬ Quantidade (mL ou g): "))
                    print("_______________________________________________________________________________\n")
                    if quant:
                        gerenciador.atualizar_quantidade(id, quant)
                        time.sleep(3)
                        limpar_tela()
                        menu_principal(db)

                    else:
                        print("ERRO: quantidade sem dados, escreva algum valor...")
                        time.sleep(3)
                        limpar_tela()
                        menu_principal(db)

                except Exception as error:
                    print(f"ERRO: Nâo foi possivel iniciar opçção! -> {error}\n")
                    time.sleep(3)
                    opcoes_principal(db)

            case "5":
                try:
                    limpar_tela()
                    print("_______________________________________________________________________________\n")
                    subs = input("[*] Qual Substância deseja DELETAR?\n[DIGITE o ID da Substância]: ")
                    if subs:
                        gerenciador.deletar_substancia(subs)
                        print("_______________________________________________________________________________\n")
                        time.sleep(3)
                        limpar_tela()
                        menu_principal(db)
                    else:
                        print("ERRO: Insira um ID da Substância que deseja excluir!\n")
                        time.sleep(3)
                        limpar_tela()
                        menu_principal(db)

                except Exception as error:
                    print(f"ERRO: Falha ao excluir Substância! -> {error}, Tente Novamente...\n")
                    time.sleep(3)
                    limpar_tela()
                    opcoes_principal(db)

            case "6":
                try:
                    print("_______________________________________________________________________________\n")
                    resp = input("[!] Tem certeza que deseja limpar o Banco de Dados?\n[Essa Ação não poderá ser Desfeita]\n\n[1]¬ Sim\n[2]¬ Não\nOPÇÃO: ")
                    if resp == "1":
                        print("_______________________________________________________________________________\n")
                        print("                 ---------   EXCLUINDO BANCO DE DADOS   ---------              \n")
                        db.deletar_todas_substancias()
                        time.sleep(3)
                        limpar_tela()
                        menu_principal(db)
                    elif resp == "2":
                        print("_______________________________________________________________________________\n")
                        time.sleep(1.5)
                        limpar_tela()
                        menu_principal(db)
                    else:
                        print("ERRO: Dados Informados Incorretamente! Tente Novamente...\n")
                        time.sleep(3)
                        limpar_tela()
                        menu_principal(db)

                except Exception as error:
                    print(f"ERRO: Falha ao limpar Banco de Dados! -> {error}\n")
                    time.sleep(3)
                    opcoes_principal(db)

            case "7":
                try:
                    print("_______________________________________________________________________________\n")
                    print("\n              ---------   FECHANDO BioStock Manager   ---------              \n")
                    time.sleep(3)
                    print("_______________________________________________________________________________\n")
                    sys.exit()
                except Exception as error:
                    print("________________________________________________________________________________\n")
                    print(f"\nERRO: {error}! Apenas Feche o Programa.\n")
                    print("________________________________________________________________________________\n")
                    time.sleep(5)
                    limpar_tela()
                    menu_principal(db)
    except Exception as error:
        print(f"ERRO: Falha ao iniciar o Menu Principal -> {error}. Tentando Novamente...")
        time.sleep(3)
        limpar_tela()
        menu_principal(db)


def menu_principal(db):
    print("\n ███████████   ███            █████████   █████                      █████     \n░░███░░░░░███ ░░░            ███░░░░░███ ░░███                      ░░███      \n ░███    ░███ ████   ██████ ░███    ░░░  ███████    ██████   ██████  ░███ █████\n ░██████████ ░░███  ███░░███░░█████████ ░░░███░    ███░░███ ███░░███ ░███░░███ \n ░███░░░░░███ ░███ ░███ ░███ ░░░░░░░░███  ░███    ░███ ░███░███ ░░░  ░██████░  \n ░███    ░███ ░███ ░███ ░███ ███    ░███  ░███ ███░███ ░███░███  ███ ░███░░███ \n ███████████  █████░░██████ ░░█████████   ░░█████ ░░██████ ░░██████  ████ █████\n░░░░░░░░░░░  ░░░░░  ░░░░░░   ░░░░░░░░░     ░░░░░   ░░░░░░   ░░░░░░  ░░░░ ░░░░░ \n")
    print("                  _  _ ____ _  _ ____ ____ ____ ____ \n                  |\/| |__| |\ | |__| | __ |___ |__/ \n                  |  | |  | | \| |  | |__] |___ |  \ \n")
    print("              ---------------   [ MENU ]   ---------------              \n")
    print("[!] OPÇÕES:\n")
    print("º [1]¬ ADICIONAR substância.")
    print("º [2]¬ PESQUISAR substância.")
    print("º [3]¬ LISTAR todo o estoque.")
    print("º [4]¬ ATUALIZAR quantidade da substância.")
    print("º [5]¬ DELETAR uma substância.")
    print("º [6]¬ DELETAR todo o banco de dados. (CUIDADO !)")
    print("º [7]¬ FECHAR programa.\n")
    opcoes_principal(db)


if __name__ == "__main__":
    try:
        database()
        db = Database("BioStock.db")
        gerenciador = GerenciadorStock(db)
        menu_principal(db)
    except sqlite3.Error as sql_error:
        print(f"ERRO: Banco de Dados! -> {sql_error}\n")
        time.sleep(30)
        sys.exit()

    except Exception as generic_error:
        print(f"ERRO: Falha ao Iniciar o Programa -> {generic_error}\n")
        time.sleep(30)
        sys.exit()
