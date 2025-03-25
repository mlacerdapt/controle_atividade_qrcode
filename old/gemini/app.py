from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import qrcode
import io
from base64 import b64encode
import datetime

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))

@app.route('/')
def index():
    return render_template('index.html')

# Funções de cadastro (funcionário, área, equipamento) e registro de tarefas

def gerar_qrcode(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_base64 = b64encode(img_buffer.getvalue()).decode('utf8')
    return img_base64

@app.route('/cadastro_funcionario')
def cadastro_funcionario():
    return render_template('cadastro_funcionario.html')

@app.route('/cadastrar_funcionario', methods=['POST'])
def cadastrar_funcionario():
    numero_sap = request.form['numero_sap']
    nome = request.form['nome']
    conn = get_db_connection()
    conn.execute('INSERT INTO funcionario (numero_sap, nome) VALUES (?, ?)', (numero_sap, nome))
    conn.commit()
    conn.close()
    qrcode_base64 = gerar_qrcode(numero_sap)
    return render_template('qrcode.html', qrcode=qrcode_base64)
    
@app.route('/cadastro_area')
def cadastro_area():
    return render_template('cadastro_area.html')

@app.route('/cadastrar_area', methods=['POST'])
def cadastrar_area():
    codigo = request.form['codigo']
    nome = request.form['nome']
    descricao = request.form['descricao']
    conn = get_db_connection()
    conn.execute('INSERT INTO area (codigo, nome, descricao) VALUES (?, ?, ?)', (codigo, nome, descricao))
    conn.commit()
    conn.close()
    qrcode_base64 = gerar_qrcode(codigo)
    return render_template('qrcode.html', qrcode=qrcode_base64)

@app.route('/cadastro_equipamento')
def cadastro_equipamento():
    return render_template('cadastro_equipamento.html')

@app.route('/cadastrar_equipamento', methods=['POST'])
def cadastrar_equipamento():
    codigo = request.form['codigo']
    nome = request.form['nome']
    descricao = request.form['descricao']
    conn = get_db_connection()
    conn.execute('INSERT INTO equipamento (codigo, nome, descricao) VALUES (?, ?, ?)', (codigo, nome, descricao))
    conn.commit()
    conn.close()
    qrcode_base64 = gerar_qrcode(codigo)
    return render_template('qrcode.html', qrcode=qrcode_base64)

@app.route('/registrar_tarefa')
def registrar_tarefa():
    return render_template('registrar_tarefa.html')

@app.route('/iniciar_tarefa', methods=['POST'])
def iniciar_tarefa():
    funcionario_codigo = request.form['funcionario_codigo']
    area_codigo = request.form['area_codigo']
    equipamento_codigo = request.form['equipamento_codigo']

    conn = get_db_connection()

    funcionario = conn.execute('SELECT id FROM funcionario WHERE numero_sap = ?', (funcionario_codigo,)).fetchone()
    area = conn.execute('SELECT id FROM area WHERE codigo = ?', (area_codigo,)).fetchone()
    equipamento = conn.execute('SELECT id FROM equipamento WHERE codigo = ?', (equipamento_codigo,)).fetchone()

    if funcionario and area and equipamento:
        conn.execute('INSERT INTO tarefa (funcionario_id, area_id, equipamento_id, data_hora_inicio) VALUES (?, ?, ?, ?)',
                     (funcionario['id'], area['id'], equipamento['id'], datetime.datetime.now()))
        conn.commit()
        conn.close()
        return "Tarefa iniciada com sucesso!"
    else:
        conn.close()
        return "Códigos inválidos!"

@app.route('/finalizar_tarefa', methods=['POST'])
def finalizar_tarefa():
    funcionario_codigo = request.form['funcionario_codigo']

    conn = get_db_connection()

    funcionario = conn.execute('SELECT id FROM funcionario WHERE numero_sap = ?', (funcionario_codigo,)).fetchone()

    if funcionario:
        conn.execute('UPDATE tarefa SET data_hora_fim = ? WHERE funcionario_id = ? AND data_hora_fim IS NULL', (datetime.datetime.now(), funcionario['id']))
        conn.commit()
        conn.close()
        return "Tarefa finalizada com sucesso!"
    else:
        conn.close()
        return "Código de funcionário inválido!"
    


if __name__ == '__main__':
    init_db()
    app.run(debug=True)