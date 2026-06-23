import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()


def listar_usuarios():
    """Função auxiliar para exibir os usuários disponíveis antes das ações"""
    try:
        cursor.execute("SELECT id, nome FROM usuarios")
        usuarios = cursor.fetchall()
        if usuarios:
            print("\n--- Usuários Cadastrados ---")
            for u in usuarios:
                print(f"ID: {u[0]} | Nome: {u[1]}")
            print("")
        else:
            print("Nenhum usuário cadastrado no sistema.")
    except sqlite3.OperationalError:
        print("[Aviso] Tabela de usuários não encontrada.")


def listar_habitos_por_usuario(usuario_id):
    """Função auxiliar para listar hábitos de um usuário e validar sua existência"""
    cursor.execute(
        "SELECT id, nome, descricao, frequencia, meta FROM habitos WHERE usuario_id=?",
        (usuario_id,)
    )
    dados = cursor.fetchall()

    if len(dados) == 0:
        print(f"\nNenhum hábito encontrado para o usuário com ID {usuario_id}.\n")
        return False
    else:
        print(f"\n--- Hábitos do Usuário {usuario_id} ---")
        for habito in dados:
            print(f"ID Hábito: {habito[0]} | Nome: {habito[1]} | Descrição: {habito[2]} | Freq: {habito[3]} | Meta: {habito[4]}")
        print("")
        return True


def cadastrar():
    print("CADASTRAR HÁBITO")
    listar_usuarios()
    usuario_id = int(input("Digite o ID do usuário dono do hábito: "))
    
    nome = input("Nome do hábito: ")
    descricao = input("Descrição (opcional): ")

    print("Escolha a frequência:")
    print("1 - Diária")
    print("2 - Semanal")
    print("3 - Mensal")
    op = input("Opção: ")

    if op == "1":
        frequencia = "Diária"
    elif op == "2":
        frequencia = "Semanal"
    else:
        frequencia = "Mensal"

    meta = int(input("Meta (número de vezes): "))

    cursor.execute(
        "INSERT INTO habitos(usuario_id, nome, descricao, frequencia, meta) VALUES(?,?,?,?,?)",
        (usuario_id, nome, descricao, frequencia, meta)
    )
    
    conexao.commit()
    print("Hábito cadastrado com sucesso!\n")


def listar():
    print("LISTAR HÁBITOS")
    listar_usuarios()
    usuario = int(input("Digite o ID do usuário para ver os hábitos: "))
    listar_habitos_por_usuario(usuario)


def editar():
    print("EDITAR HÁBITO ")
    listar_usuarios()
    usuario_id = int(input("Digite o ID do usuário: "))
    
    if not listar_habitos_por_usuario(usuario_id):
        return

    id_habito = int(input("Digite o ID do hábito que deseja alterar: "))

    cursor.execute(
        "SELECT nome, descricao, frequencia, meta FROM habitos WHERE id=? AND usuario_id=?",
        (id_habito, usuario_id)
    )
    habito = cursor.fetchone()

    if habito is None:
        print("Hábito não encontrado para este usuário.")
        return

    print("\n(Pressione ENTER sem digitar nada para manter o valor atual)")
    nome = input(f"Nome [{habito[0]}]: ")
    descricao = input(f"Descrição [{habito[1]}]: ")
    frequencia = input(f"Frequência [{habito[2]}]: ")
    meta = input(f"Meta [{habito[3]}]: ")

    if nome == "": nome = habito[0]
    if descricao == "": descricao = habito[1]
    if frequencia == "": frequencia = habito[2]
    if meta == "": meta = habito[3]

    cursor.execute("""
        UPDATE habitos
        SET nome=?, descricao=?, frequencia=?, meta=?
        WHERE id=?
    """, (nome, descricao, frequencia, meta, id_habito))

    conexao.commit()
    print("Hábito atualizado com sucesso!\n")


def deletar():
    print(" DELETAR HÁBITO")
    listar_usuarios()
    usuario_id = int(input("Digite o ID do usuário: "))
    
    if not listar_habitos_por_usuario(usuario_id):
        return

    id_habito = int(input("Digite o ID do hábito que deseja excluir: "))
    confirma = input(f"Deseja realmente excluir o hábito {id_habito} e todos os seus registros vinculados? (s/n): ")

    if confirma.lower() == "s":
        cursor.execute(
            "DELETE FROM registros WHERE habito_id=?",
            (id_habito,)
        )

        cursor.execute(
            "DELETE FROM habitos WHERE id=?",
            (id_habito,)
        )
        
        conexao.commit()
        print("Hábito e registros vinculados excluídos com sucesso.\n")
    else:
        print("Operação cancelada.\n")



while True:
    print(" HÁBITOS")
    print("1 - Cadastrar Hábito")
    print("2 - Listar Hábitos")
    print("3 - Editar Hábito")
    print("4 - Deletar Hábito")
    print("0 - Sair")

    op = input("Escolha uma opção: ")

    if op == "1":
        cadastrar()
    elif op == "2":
        listar()
    elif op == "3":
        editar()
    elif op == "4":
        deletar()
    elif op == "0":
        print("Encerrando o programa... Até logo!")
        break
    else:
        print("Opção inválida! Tente novamente.\n")

conexao.close()