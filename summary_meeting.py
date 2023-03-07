from flask import Flask, render_template, request, flash
import pyperclip

app = Flask(__name__)
app.secret_key = 'chave_secreta'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generate_summary():
    titulo_da_reuniao = request.form.get('titulo', '')
    data_da_reuniao = request.form.get('data', '')
    participantes = request.form.getlist('participantes')
    notas_da_reuniao = request.form.getlist('notas')
    gerente_responsavel = request.form.get('gerente', 'Desconhecido')
    pendencias = request.form.get('pendencias', '')
    botmanager_ok = request.form.get('botmanager_ok', 'Desconhecido')
    sucesso_da_reuniao = request.form.get('sucesso', '')
    hora_de_termino = request.form.get('hora_de_termino', '')

    # Gerando resumo em texto simples
    resumo = f"Título da Reunião: {titulo_da_reuniao}\n"
    resumo += f"Data da Reunião: {data_da_reuniao}\n"
    resumo += f"Participantes: {', '.join(participantes)}\n"
    resumo += f"Notas da Reunião:\n"
    for i, nota in enumerate(notas_da_reuniao):
        resumo += f"  Discussão {i+1}: {nota}\n"
    resumo += f"Gerente Responsável pelos Testes: {gerente_responsavel}\n"
    resumo += f"Pendências: {pendencias}\n"
    resumo += f"O Botmanager Está Funcionando Corretamente?: {botmanager_ok}\n"
    resumo += f"Sucesso da Reunião: {sucesso_da_reuniao}\n"
    resumo += f"Hora de Término da Reunião: {hora_de_termino}\n"

    # Copiando resumo para a área de transferência
    pyperclip.copy(resumo)

    return render_template('index.html', summary=resumo)

if __name__ == '__main__':
    app.run(debug=True)
