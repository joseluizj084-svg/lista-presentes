from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segredo-lista'
socketio = SocketIO(app, cors_allowed_origins="*")

ARQUIVO_PRESENTES = "presentes.json"

categorias_iniciais = {
    "Cozinha": [
        "Açucareiro","Abridor de latas","Amassador de alho","Amassador de batata","Avental","Canecas",
        "Centrifuga de salada","Colher de arroz","Colher de sorvete","Colheres de medida","Colheres de pau ou silicone",
        "Concha","Cortador de pizza ou bolo","Cumbucas","Cuscuzeira","Descanso de panela","Descascador",
        "Escorredor de massa","Escorredor de louças","Escumadeira","Espátula","Forma de bolo","Garrafa térmica",
        "Jogo americano","Jogo de copos","Jogo de facas","Jogo de louça","Jogo de panelas","Jogo de taças",
        "Jogo de xícaras","Lixeira com tampa","Medidor de alimentos","Panela de pressão","Panos de pratos",
        "Passadeiras","Pegador de massa","Peneira","Porta azeite","Potes","Prato de bolo","Ralador",
        "Rolo de massa","Saladeira","Saleiro","Tábua de corte","Taças de servir","Tesoura de cozinha",
        "Tigelas","Toalha de mesa (4 lugares quadrada)"
    ],
    "Lavanderia": [
        "Baldes","Cesto de roupas","Escova","Ferro de passar","Pá","Pano de chão",
        "Pregadores","Rodo","Tábua de passar","Varal de roupa","Vassoura"
    ],
    "Banheiro": [
        "Escova para sanitário","Jogo de tapetes","Lixeira pequena","Porta escova de dentes",
        "Porta algodão","Porta cotonetes","Saboneteira","Toalhas de banho","Toalhas de mão"
    ],
    "Quarto": [
        "Cobre leito (Colchão casal padrão, altura 30cm)",
        "Colcha (Colchão casal padrão, altura 30cm)",
        "Fronhas",
        "Lençol com elástico (Colchão casal padrão, altura 30cm)",
        "Lençol sem elástico (Colchão casal padrão, altura 30cm)",
        "Protetor de colchão (Colchão casal padrão, altura 30cm)"
    ]
}

if not os.path.exists(ARQUIVO_PRESENTES):
    presentes = {cat: [{"nome": item, "escolhido": False} for item in itens]
                 for cat, itens in categorias_iniciais.items()}
    json.dump(presentes, open(ARQUIVO_PRESENTES, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
else:
    presentes = json.load(open(ARQUIVO_PRESENTES, encoding="utf-8"))

def salvar():
    json.dump(presentes, open(ARQUIVO_PRESENTES, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html', presentes=presentes)

@socketio.on('escolher_presente')
def escolher_presente(data):
    categoria = data.get("categoria")
    nome = data.get("nome")
    for p in presentes[categoria]:
        if p["nome"] == nome and not p["escolhido"]:
            p["escolhido"] = True
            salvar()
            emit('atualizar_lista', presentes, broadcast=True)
            break

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
