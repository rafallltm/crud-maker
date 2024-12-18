import sqlite3

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect("tarefas.db")

# Função para criar a tabela de tarefas se ainda não existir
def criar_tabela(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            concluida INTEGER
        )
    ''')

# Função para criar uma nova tarefa
def criar_tarefa(cursor, descricao):
    cursor.execute("INSERT INTO tarefas (descricao, concluida) VALUES (?, 0)", (descricao,))

# Função para ler todas as tarefas
def ler_tarefas(cursor):
    cursor.execute("SELECT * FROM tarefas")
    return cursor.fetchall()

# Função para atualizar uma tarefa
def atualizar_tarefa(cursor, id, concluida):
    cursor.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (concluida, id))

# Função para excluir uma tarefa
def excluir_tarefa(cursor, id):
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))

# Função principal
def main():
    conn = conectar_bd()
    cursor = conn.cursor()
    criar_tabela(cursor)

    while True:
        print("\nAplicativo de Gerenciamento de Tarefas")
        print("1. Criar Tarefa")
        print("2. Listar Tarefas")
        print("3. Marcar Tarefa como Concluída")
        print("4. Excluir Tarefa")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        try:
            if escolha == "1":
                descricao = input("Digite a descrição da tarefa: ")
                criar_tarefa(cursor, descricao)
                conn.commit()
                print("Tarefa criada com sucesso!")

            elif escolha == "2":
                tarefas = ler_tarefas(cursor)
                print("\nLista de Tarefas:")
                for tarefa in tarefas:
                    status = "Concluída" if tarefa[2] else "Pendente"
                    print(f"{tarefa[0]}. {tarefa[1]} - {status}")

            elif escolha == "3":
                id = int(input("Digite o ID da tarefa a ser marcada como concluída: "))
                atualizar_tarefa(cursor, id, 1)
                conn.commit()
                print("Tarefa marcada como concluída!")

            elif escolha == "4":
                id = int(input("Digite o ID da tarefa a ser excluída: "))
                excluir_tarefa(cursor, id)
                conn.commit()
                print("Tarefa excluída com sucesso!")

            elif escolha == "5":
                print("Saindo do aplicativo.")
                break

            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    conn.close()

if __name__ == "__main__":
    main()
