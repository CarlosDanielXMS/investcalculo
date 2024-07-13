from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

banco_dados = 'bd.txt'

def read_file():
    with open(banco_dados, 'r') as bd:
        return [line.strip().split(',') for line in bd]

def write_file(lines):
    with open(banco_dados, 'w') as bd:
        for i, line in enumerate(lines):
            if i == 0:
                bd.write(','.join(line))
            else:
                bd.write("\n" + ','.join(line))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    bd = read_file()
    email = request.form['email']
    password = request.form['password']

    for linha in bd:
        if len(linha) >= 3 and email == linha[1] and password == linha[2]:
            return jsonify(status='success', message='Login executado com Sucesso!')
    return jsonify(status='error', message='Email ou senha Inválidos')

@app.route('/registrar', methods=['POST'])
def registrar():
    bd = read_file()
    usuario = request.form['usuario']
    email = request.form['email']
    senha = request.form['password']

    for linha in bd:
        if len(linha) >= 2 and email == linha[1]:
            return jsonify(status='error', message='Email já cadastrado!')

    registro = [usuario, email, senha]
    bd.append(registro)
    write_file(bd)

    return jsonify(status='success', message='Registro efetuado com sucesso!')

if __name__ == '__main__':
    app.run(debug=True)
