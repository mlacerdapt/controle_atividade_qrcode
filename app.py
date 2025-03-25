from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import qrcode
from datetime import datetime
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'

# Criação do Banco de Dados
def criar_banco():
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS funcionario (id INTEGER PRIMARY KEY, nome TEXT, numero_sap TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS area (id INTEGER PRIMARY KEY, nome TEXT, codigo TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS equipamento (id INTEGER PRIMARY KEY, nome TEXT, codigo TEXT)''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tarefa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_qr TEXT,
            equipamento_qr TEXT,
            funcionario_qr TEXT,
            data_inicio TEXT,
            funcionario_finalizou TEXT,
            data_fim TEXT
        )
    ''')
    conn.commit()
    conn.close()
def gerar_qrcode(conteudo, nome_arquivo):
    qr = qrcode.make(conteudo)
    if not os.path.exists('static/qrcodes'):
        os.makedirs('static/qrcodes')
    qr.save(f'static/qrcodes/{nome_arquivo}.png')

# Rota inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para cadastrar funcionário
@app.route('/cadastrar_funcionario', methods=['GET', 'POST'])
def cadastrar_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        numero_sap = request.form['numero_sap']
        id_funcionario = request.form['id']  # Aqui você deve obter o ID do funcionário

        # Adiciona o funcionário ao banco de dados (ou algum outro processo)
        # Exemplo: db.session.add(funcionario)
        # db.session.commit()

        # Chama a função para gerar o QR Code com o id do funcionário
        gerar_qrcode(numero_sap, f'funcionario_{numero_sap}', id_funcionario)

        return redirect(url_for('funcionarios'))  # Redireciona para a lista de funcionários

    return render_template('cadastrar_funcionario.html')

# Rota para cadastrar área
@app.route('/cadastrar_area', methods=['GET', 'POST'])
def cadastrar_area():
    if request.method == 'POST':
        nome = request.form['nome']
        codigo = request.form['codigo']

        conn = sqlite3.connect('sistema.db')
        c = conn.cursor()
        c.execute("INSERT INTO area (nome, codigo) VALUES (?, ?)", (nome, codigo))
        conn.commit()
        conn.close()

        gerar_qrcode(codigo, f'area_{codigo}')

        flash('Área cadastrada com sucesso!')
        return redirect(url_for('home'))
    return render_template('cadastrar_area.html')

# Rota para cadastrar equipamento
@app.route('/cadastrar_equipamento', methods=['GET', 'POST'])
def cadastrar_equipamento():
    if request.method == 'POST':
        nome = request.form['nome']
        codigo = request.form['codigo']

        conn = sqlite3.connect('sistema.db')
        c = conn.cursor()
        c.execute("INSERT INTO equipamento (nome, codigo) VALUES (?, ?)", (nome, codigo))
        conn.commit()
        conn.close()

        gerar_qrcode(codigo, f'equipamento_{codigo}')

        flash('Equipamento cadastrado com sucesso!')
        return redirect(url_for('home'))
    return render_template('cadastrar_equipamento.html')

# Rota para cadastrar tarefa
@app.route('/registrar_tarefa', methods=['GET', 'POST'])
def registrar_tarefa():
    if request.method == 'POST':
        area_qr = request.form.get('area_qr')
        equipamento_qr = request.form.get('equipamento_qr')
        funcionario_qr = request.form.get('funcionario_qr')

        # Registra as informações no banco de dados
        conn = sqlite3.connect('sistema.db')
        c = conn.cursor()
        data_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Inserção do registro da tarefa
        c.execute("INSERT INTO tarefa (area_qr, equipamento_qr, funcionario_qr, data_inicio) VALUES (?, ?, ?, ?)",
            (area_qr, equipamento_qr, funcionario_qr, data_inicio)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('registrar_tarefa.html')


# Rota para consultar funcionários
@app.route('/relatorio_funcionarios')
def relatorio_funcionarios():
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute("SELECT * FROM funcionario")
    funcionarios = c.fetchall()
    conn.close()
    return render_template('relatorio_funcionarios.html', funcionarios=funcionarios)

# Rota para consultar áreas
@app.route('/relatorio_areas')
def relatorio_areas():
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute("SELECT * FROM area")
    areas = c.fetchall()
    conn.close()
    return render_template('relatorio_areas.html', areas=areas)

# Rota para consultar equipamentos
@app.route('/relatorio_equipamentos')
def relatorio_equipamentos():
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()
    c.execute("SELECT * FROM equipamento")
    equipamentos = c.fetchall()
    conn.close()
    return render_template('relatorio_equipamentos.html', equipamentos=equipamentos)

@app.route('/finalizar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def finalizar_tarefa(tarefa_id):
    if request.method == 'POST':
        # Recebe o QR Code do funcionário
        funcionario_qr = request.form.get('funcionario_qr')

        # Atualiza a tarefa no banco de dados para marcar como finalizada
        conn = sqlite3.connect('sistema.db')
        c = conn.cursor()
        data_fim = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("""
            UPDATE tarefa 
            SET funcionario_finalizou = ?, data_fim = ?
            WHERE id = ?
        """, (funcionario_qr, data_fim, tarefa_id))
        conn.commit()
        conn.close()

        # Redireciona de volta à página inicial após a finalização
        return redirect('/')

    return render_template('finalizar_tarefa.html', tarefa_id=tarefa_id)

@app.route('/excluir/<tipo>/<int:id>', methods=['GET'])
def excluir(tipo, id):
    conn = sqlite3.connect('sistema.db')
    c = conn.cursor()

    # Caminho do arquivo QR Code
    qrcode_path = f"static/qrcodes/{tipo}_{id}.png"

    if tipo == 'funcionario':
        # Obtém o QR Code do funcionário do banco de dados
        c.execute("SELECT qrcode FROM funcionario WHERE id = ?", (id,))
        funcionario = c.fetchone()
        if funcionario:
            qrcode_path = os.path.join('static', 'qrcodes', funcionario[0])

        # Exclui o funcionário do banco de dados
        c.execute("DELETE FROM funcionario WHERE id = ?", (id,))
    
    elif tipo == 'area':
        # Obtém o QR Code da área do banco de dados
        c.execute("SELECT qrcode FROM area WHERE id = ?", (id,))
        area = c.fetchone()
        if area:
            qrcode_path = os.path.join('static', 'qrcodes', area[0])

        # Exclui a área do banco de dados
        c.execute("DELETE FROM area WHERE id = ?", (id,))
    
    elif tipo == 'equipamento':
        # Obtém o QR Code do equipamento do banco de dados
        c.execute("SELECT qrcode FROM equipamento WHERE id = ?", (id,))
        equipamento = c.fetchone()
        if equipamento:
            qrcode_path = os.path.join('static', 'qrcodes', equipamento[0])

        # Exclui o equipamento do banco de dados
        c.execute("DELETE FROM equipamento WHERE id = ?", (id,))

    # Se o QR Code existir, remove o arquivo
    if qrcode_path and os.path.exists(qrcode_path):
        os.remove(qrcode_path)

    conn.commit()
    conn.close()

    # Redireciona para a página de relatórios após a exclusão
    return redirect(f'/{tipo}_relatorio')

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)
