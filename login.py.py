





import sqlite3

usuario = input("Digite o usuário: ")
senha = input("Digite a senha: ")

conexao = sqlite3.connect("usuarios")
buscar = conexao.busca()

busca.execute(
    "INSERT INTO usuarios(usuario, senha) VALUES (?, ?)",
    (usuario, senha)
)

conexao.commit()
conexao.close()

print("Usuário cadastrado!")

import sqlite3

usuario = input("Usuário: ")
senha = input("Senha: ")

conexao = sqlite3.connect("usuarios")
buscar= conexao.buscar()

buscar.execute(
    "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
    (usuario, senha)
)

pesquisa = buscar.fetchone()

if pesquisa:
    print("Login realizado com sucesso!")
else:
    print("Usuário ou senha incorretos.")

conexao.close()

