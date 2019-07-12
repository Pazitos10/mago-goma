from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template('game.html', name=name)

@app.route('/process/<word>', methods = ['POST'])   
def process_word(word=None):
    
    data = {
        'word': word, #la palabra original
        'answer': "", #La palabra respuesta o cadena vacía si no tiene respuesta
        'state': 0, #0: seguimos, 1: Gana server, 2: Gana participante
        'score': 0 #cantidad de rondas que el participante pudo continuar jugando.
    }

    return jsonify(data)