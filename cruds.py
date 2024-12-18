from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect("tarefas.db")

# Função para criar a tabela de tarefas se ainda não existir
def criar_tabela():
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT,
                concluida INTEGER
            )
        ''')

# Rota para listar tarefas
@app.route("/")
def listar_tarefas():
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarefas")
        tarefas = cursor.fetchall()
    return render_template("index.html", tarefas=tarefas)

# Rota para adicionar uma tarefa
@app.route("/adicionar", methods=["POST"])
def adicionar_tarefa():
    descricao = request.form.get("descricao")
    if descricao:
        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tarefas (descricao, concluida) VALUES (?, 0)", (descricao,))
            conn.commit()
    return redirect("/")

# Rota para concluir uma tarefa
@app.route("/concluir/<int:tarefa_id>")
def concluir_tarefa(tarefa_id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (tarefa_id,))
        conn.commit()
    return redirect("/")

# Rota para excluir uma tarefa
@app.route("/excluir/<int:tarefa_id>")
def excluir_tarefa(tarefa_id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        conn.commit()
    return redirect("/")

if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
