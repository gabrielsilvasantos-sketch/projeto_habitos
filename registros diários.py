import sqlite3
from banco import  conectar

def criar_registro():
    print("---------- Novo Registro de Hábito ----------")
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        id_usuario = int(input("ID do usuário: "))
        nome_usuario = input("Nome do usuário: ").lower()
        
        cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (id_usuario,))
        usuario = cursor.fetchone()
        if usuario is None:
            print("ID não encontrado.")
            conn.close()
            return None

        if usuario["nome"].lower() != nome_usuario:
            print("O nome informado não corresponde ao ID")
            conn.close()
            return None

        id_habito = int(input("ID do hábito: "))
        cursor.execute('SELECT nome FROM habitos WHERE id = ? AND id_usuario = ?', (id_habito, id_usuario))

        habito = cursor.fetchone()
        if habito is None:
            print("ID do hábito não encontrado ou não pertencente ao usuário informado.")
            conn.close()
            return None

        print(f"Hábito selecionado: {habito['nome']}")

        data = input("Data da prática do hábito (AAAA-MM-DD): ")
        status = input("Status: (ex.: 'Concluído', 'Não concluído', 'Parcialmente concluído') ")
        observacao = input("Observações: ")

        cursor.execute("""
        INSERT INTO registros
        (id_usuario, id_habito, data, status, observacao)
        VALUES (?, ?, ?, ?, ?)
        """, (id_usuario, id_habito, data, status, observacao))

        conn.commit()
        conn.close()

        return{
            "id_usuario": id_usuario,
            "id_habito" : id_habito,
            "data" : data,
            "status" : status,
            "observacao" : observacao
        }
    except Exception as erro:
        print(f"Erro ao criar registro: {erro}.")
        return None


def ler_registros():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT R.*, H.nome AS nome_habito
            FROM registros R
            INNER JOIN habitos H ON R.id_habito = H.id
            ORDER BY R.id DESC
            """)

    registros = cursor.fetchall()
    if not registros:
        print("Nenhum registro cadastrado.\n")
        conn.close()
        return

    print("\n-------------Registros cadastrados-------------\n")
    for registro in registros:
        print(
            f"ID do hábito: {registro['id_habito']} |\n {registro['status']}\n"
            f"{registro['data']}\n"
            f"Observação: {registro['observacao']}\n")

    conn.close()


def ler_um():
    conn = conectar()
    cursor = conn.cursor()

    try:
        id_registro = int(input("Digite o ID do registro: "))

        cursor.execute("""
            SELECT R.*, H.nome AS nome_habito
            FROM registros R
            INNER JOIN habitos H ON R.id_habito = H.id
            WHERE R.id = ?
            """, (id_registro,))

        registro = cursor.fetchone()

        
        if registro:
            print("\n---------- Detalhes do Registro ----------\n")
            print(f"Registro do Hábito: {registro['nome_habito']}")
            print(f"Data: {registro['data']}")
            print(f"Status: {registro['status']}")
            print(f"Observação: {registro['observacao']}\n")
            return
        else:
            print("Registro não encontrado.\n")

    except ValueError:
        print("ID inválido.\n")
    finally:
        conn.close()


def atualizar_registro():
    conn = conectar()
    cursor = conn.cursor()

    try:
        id_registro = int(input("Informe o ID  do registro que deseja atualizar: "))
        
        cursor.execute('SELECT * FROM registros WHERE id = ?', (id_registro,))
        registro = cursor.fetchone()

        if not registro:
            print("\nRegistro não encontrado\n")
            return

        print("----- Dados do Registro Atual -----")
        print(f"ID hábito: {registro['id_habito']}")
        print(f"\nID do registro: {registro['id']}")
        print(f"Data: {registro['data']}")
        print(f"Observação: {registro['observacao']}")

        print("\n---------- Atualização do registro ----------\n")
        nova_data = input("Nova data (AAAA-MM-DD): ")
        novo_status = input("Novo status ('Concluído', 'Não concluído', 'Parcialmente concluído'): ")
        nova_observacao = input("Nova observação: ")

        cursor.execute("""
        UPDATE registros
        SET data = ?, 
        status = ?, 
        observacao = ?
        WHERE id = ?""", (nova_data, novo_status, nova_observacao, id_registro))

        conn.commit()
        print("\nRegistro atualizado com sucesso!")

    except ValueError:
        print("Id inválido.")
    finally:
        conn.close()


def deletar_registro():
    conn = conectar()
    cursor = conn.cursor()

    try:
        print("----------Deletar Registro ----------")
        cursor.execute("""
        SELECT R.*, H.nome AS nome_habito
        FROM registros R
        INNER JOIN habitos H ON R.id_habito = H.id
        """)
        registros = cursor.fetchall()

        if not registros:
            print("Nenhum registro cadastrado.\n")
            return

        id_registro = int(input("Informe o ID do registro que deseja deletar: "))

        registro_encontrado = None
        for registro in registros:
            if registro["id"] == id_registro:
                registro_encontrado = registro
                break

        if registro_encontrado is None:
            print("\nO ID informado não foi cadastrado.\n")
            return
        
        print("\n---------- Detalhes do Registro ----------\n")
        print(f"Registro do Hábito: {registro_encontrado['nome_habito']}")
        print(f"Data: {registro_encontrado['data']}")
        print(f"Status: {registro_encontrado['status']}")
        print(f"Observação: {registro_encontrado['observacao']}\n")
                    
        confirmar = input("Tem certeza que deseja deletar este registro? (s/n): ").lower()
        if confirmar != 's':
            print("Operação cancelada.\n")
            return

        cursor.execute("""
        DELETE FROM registros WHERE id = ?""", (id_registro,))
        conn.commit()

        print("Registro deletado com sucesso!")

    except ValueError:
        print("Erro: O ID deve ser um número inteiro válido.\n")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}\n")
    finally:
        conn.close()
