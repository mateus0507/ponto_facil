
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Necessário para flash e sessão

DB_FILE = "banco.db"
SQL_FILE = "banco.sql"

# Função para conectar ao banco
def conectar():
    return sqlite3.connect(DB_FILE)

# Função para criar o banco e executar o SQL se não existir
def inicializar_banco():
    if not os.path.exists(DB_FILE):
        conn = conectar()
        cursor = conn.cursor()
        with open(SQL_FILE, "r", encoding="utf-8") as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Banco criado com sucesso!")
    else:
        print("Banco já existe, nada a fazer.")

# Página inicial (login)
@app.route('/', methods=["GET", "POST"])
def pg_login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conn.close()

        

        if usuario:
            session["matricula"] = usuario[4]  # Armazena o id do usuário na sessão
            print("Usuário autenticado:", usuario)
            print("Email do usuário:", session["matricula"])
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("pg_inicial"))
        else:
            flash("Email ou senha incorretos.", "error")
            return redirect(url_for("pg_login"))
        

    return render_template('pg_login.html')

# Cadastro de colaboradores
@app.route("/pg_cadastro", methods=["GET", "POST"])
def pg_cadastro():
    success = False
    successSenha = False
    if request.method == "POST":
        
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        matricula = request.form["matricula"]
        jornada = request.form["jornada"]
        senha = request.form["senha"]
        confirm_senha = request.form["confirm_senha"]

        if senha != confirm_senha:
            flash("As senhas não coincidem.", "error")
            successSenha = True


        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user
                (nome, cpf, email, matricula, jornada, senha)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ( nome, cpf, email, matricula, jornada, senha))
            conn.commit()
            conn.close()
            flash("Cadastro realizado com sucesso!", "success")
            success = True
            return redirect(url_for("pg_login"))
        except sqlite3.IntegrityError:
            flash("Email ou CPF já cadastrado.", "error")
            return redirect(url_for("pg_login"))

    return render_template("pg_cadastro.html", success=success, successSenha=successSenha)


@app.route("/pg_inicial")
def pg_inicial():
    return render_template("pg_inicial.html")

@app.route("/pg_senha")
def pg_senha():
    return render_template("pg_senha.html")

@app.route("/pg_mrc_ponto", methods=["GET", "POST"])
@app.route("/pg_mrc_ponto", methods=["GET", "POST"])
def pg_mrc_ponto():
    matricula = session.get("matricula")
    if not matricula:
        return redirect(url_for("pg_login"))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, jornada FROM user WHERE matricula = ?", (matricula,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("pg_login"))

    nome, jornada = usuario
    agora = datetime.now()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pontos WHERE matricula = ? AND data = ? ORDER BY id",
                   (matricula, agora.date()))
    pontos_hoje = cursor.fetchall()

    if request.method == "POST":
        if jornada.lower() == "horista":
            # Contar horas trabalhadas hoje
            entradas = [p for p in pontos_hoje if p[4] == "entrada"]
            saidas = [p for p in pontos_hoje if p[4] == "saida"]

            horas_total = 0
            for e, s in zip(entradas, saidas):
                h1 = datetime.strptime(e[3], "%H:%M")
                h2 = datetime.strptime(s[3], "%H:%M")
                horas_total += (h2 - h1).seconds / 3600

            if len(entradas) > len(saidas):
                # precisa registrar saída
                if horas_total >= 10:
                    flash("Horista já atingiu 10h hoje!", "error")
                else:
                    cursor.execute("INSERT INTO pontos (matricula, data, hora, tipo) VALUES (?, ?, ?, ?)",
                                   (matricula, agora.date(), agora.strftime("%H:%M"), "saida"))
                    conn.commit()
                    flash("Saída registrada!", "success")
            else:
                if horas_total >= 10:
                    flash("Horista não pode iniciar novo expediente hoje.", "error")
                else:
                    cursor.execute("INSERT INTO pontos (matricula, data, hora, tipo) VALUES (?, ?, ?, ?)",
                                   (matricula, agora.date(), agora.strftime("%H:%M"), "entrada"))
                    conn.commit()
                    flash("Entrada registrada!", "success")

        elif jornada.lower() == "mensalista":
            ultimo = pontos_hoje[-1] if pontos_hoje else None

            # Calcular total trabalhado até agora
            entradas = [p for p in pontos_hoje if p[4] == "entrada"]
            saidas = [p for p in pontos_hoje if p[4] == "saida"]
            horas_total = 0
            for e, s in zip(entradas, saidas):
                h1 = datetime.strptime(e[3], "%H:%M")
                h2 = datetime.strptime(s[3], "%H:%M")
                horas_total += (h2 - h1).seconds / 3600

            if not ultimo:
                # primeira batida → entrada
                cursor.execute("INSERT INTO pontos (matricula, data, hora, tipo) VALUES (?, ?, ?, ?)",
                               (matricula, agora.date(), agora.strftime("%H:%M"), "entrada"))
                conn.commit()
                flash("Entrada registrada!", "success")

            elif ultimo[4] == "entrada":
                cursor.execute("INSERT INTO pontos (matricula, data, hora, tipo) VALUES (?, ?, ?, ?)",
                               (matricula, agora.date(), agora.strftime("%H:%M"), "intervalo_inicio"))
                conn.commit()
                flash("Início do intervalo registrado!", "success")

            elif ultimo[4] == "intervalo_inicio":
                cursor.execute("INSERT INTO pontos (matricula, data, hora, tipo) VALUES (?, ?, ?, ?)",
                               (matricula, agora.date(), agora.strftime("%H:%M"), "intervalo_fim"))
                conn.commit()
                flash("Fim do intervalo registrado!", "success")

            elif ultimo[4] in ["intervalo_fim", "saida"]:
                if horas_total >= 10:  # 8h regulares + 2h extras
                    flash("Mensalista não pode ultrapassar 2h extras (10h no total).", "error")
                else:
                    cursor.execute("INSERT INTO pontos (matricula, data, hora, tipo) VALUES (?, ?, ?, ?)",
                                   (matricula, agora.date(), agora.strftime("%H:%M"), "saida"))
                    conn.commit()
                    flash("Saída registrada!", "success")

    # Buscar novamente para exibir atualizado
    cursor.execute("SELECT * FROM pontos WHERE matricula = ? AND data = ? ORDER BY id",
                   (matricula, agora.date()))
    pontos_hoje = cursor.fetchall()
    conn.close()

    return render_template("pg_mrc_ponto.html", nome=nome, jornada=jornada, pontos=pontos_hoje)


@app.route("/pg_lembrete")
def pg_lembrete():
    return render_template("pg_lembrete.html")

@app.route("/pg_justificativa")
def pg_justificativa():
    return render_template("pg_justificativa.html")

@app.route("/pg_dados_pessoais", methods=["GET", "POST"])
def pg_dados_pessoais():

    matricula = session.get("matricula")

    if not matricula:
        return redirect(url_for("pg_login"))


    if request.method == "POST":
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        nascimento = request.form.get("nascimento")  # formato: YYYY-MM-DD

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM user_complemento WHERE matricula = ?", (matricula,))
        existe = cursor.fetchone()

        if existe:
            cursor.execute("""
                UPDATE user_complemento
                SET telefone = ?, endereco = ?, nascimento = ?
                WHERE matricula = ?
            """, (telefone, endereco, nascimento, matricula))
            return redirect(url_for("pg_inicial"))
        else:
            cursor.execute("""
                INSERT INTO user_complemento (matricula, telefone, endereco, nascimento)
                VALUES (?, ?, ?, ?)
            """, (matricula, telefone, endereco, nascimento))

        conn.commit()
        cursor.close()
        conn.close()

    # Para exibir dados atuais no formulário
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT telefone, endereco, nascimento FROM user_complemento WHERE matricula = ?", (matricula,))
    dados = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("pg_dados_pessoais.html", dados=dados)   

@app.route("/pg_suporte")
def pg_suporte():
    return render_template("pg_suporte.html")

#marcação de ponto 

def marcar_ponto(matricula, tipo_ponto):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM user
            WHERE matricula = ? AND tipo_ponto = ?
        """, (matricula, tipo_ponto))
        
        usuario = cursor.fetchone()
    
        if usuario:
            if tipo_ponto == "Horista":
                
                # Aqui você cria as regras de jornada do horista
                regras = {
                    "max_horas_dia": 10,
                    "max_horas_semana": 44
                    
                }
            elif tipo_ponto == "Mensalista":
                # Aqui você cria as regras de jornada do mensalista
                regras = {
                    "max_horas_dia": 8,   # exemplo
                    "max_horas_semana": 44,
                    "max_horas_extras": 50   # exemplo
                }
            else:
                regras = {}
        else:
            regras = {}

    except Exception as e:
        regras = {}
    finally:
        conn.close()


        




if __name__ == '__main__':
    inicializar_banco()
    app.run(debug=True)

