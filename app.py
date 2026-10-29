from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "catalogo-filmes-chave")

# O banco será criado automaticamente na pasta do projeto.
DATABASE = os.path.join(os.path.dirname(__file__), "filmes.db")


def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    conexao = conectar_banco()
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            nota REAL NOT NULL CHECK (nota >= 1 AND nota <= 10)
        )
    """)
    conexao.commit()
    conexao.close()


@app.route("/")
def index():
    conexao = conectar_banco()
    filmes = conexao.execute(
        "SELECT * FROM filmes ORDER BY titulo"
    ).fetchall()
    conexao.close()
    return render_template("index.html", filmes=filmes)


@app.route("/novo", methods=["GET", "POST"])
def novo_filme():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        genero = request.form.get("genero", "").strip()
        ano_texto = request.form.get("ano", "").strip()
        nota_texto = request.form.get("nota", "").strip()

        try:
            ano = int(ano_texto)
            nota = float(nota_texto)
            if not titulo or not genero:
                raise ValueError
            if ano < 1888 or ano > 2100:
                raise ValueError
            if nota < 1 or nota > 10:
                raise ValueError
        except ValueError:
            flash("Confira os campos. A nota deve ser de 1 a 10 e o ano deve ser válido.", "erro")
            return redirect(url_for("novo_filme"))

        conexao = conectar_banco()
        conexao.execute(
            "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
            (titulo, genero, ano, nota)
        )
        conexao.commit()
        conexao.close()
        flash("Filme cadastrado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("form.html", filme=None, titulo_pagina="Cadastrar filme")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_filme(id):
    conexao = conectar_banco()
    filme = conexao.execute(
        "SELECT * FROM filmes WHERE id = ?", (id,)
    ).fetchone()
    conexao.close()

    if filme is None:
        flash("Filme não encontrado.", "erro")
        return redirect(url_for("index"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        genero = request.form.get("genero", "").strip()
        ano_texto = request.form.get("ano", "").strip()
        nota_texto = request.form.get("nota", "").strip()

        try:
            ano = int(ano_texto)
            nota = float(nota_texto)
            if not titulo or not genero:
                raise ValueError
            if ano < 1888 or ano > 2100:
                raise ValueError
            if nota < 1 or nota > 10:
                raise ValueError
        except ValueError:
            flash("Confira os campos. A nota deve ser de 1 a 10 e o ano deve ser válido.", "erro")
            return redirect(url_for("editar_filme", id=id))

        conexao = conectar_banco()
        conexao.execute("""
            UPDATE filmes
            SET titulo = ?, genero = ?, ano = ?, nota = ?
            WHERE id = ?
        """, (titulo, genero, ano, nota, id))
        conexao.commit()
        conexao.close()
        flash("Filme atualizado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("form.html", filme=filme, titulo_pagina="Editar filme")


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir_filme(id):
    conexao = conectar_banco()
    conexao.execute("DELETE FROM filmes WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    flash("Filme excluído com sucesso.", "sucesso")
    return redirect(url_for("index"))


# Cria a tabela automaticamente quando o aplicativo inicia.
criar_banco()

if __name__ == "__main__":
    app.run(debug=True)
