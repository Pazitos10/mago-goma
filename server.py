from flask import Flask, render_template, jsonify
from Game import Game, ERROR_INVALID_RULE, ERROR_WORD_USED, ERROR_UNSYLLABLE, OK, BULLSHIT


app = Flask(__name__)

def init_g():
    return Game("test_palabras_espanol.txt")

@app.route('/')
def home(name=None):
    g = init_g()
    _, word, _ = g.run()
    return render_template('game.html', name=name, word=word)

@app.route('/process/<word>', methods = ['POST'])   
def process_word(word=None):

    g = init_g()
    gamer, w, error = g.run(word)
    print(g.state.bw.last_word, w)
    
    data = {
        'word': word, #la palabra original (user)
        'answer': g.state.bw.last_word, #La palabra respuesta o cadena vacía si no tiene respuesta (server).
        'state': error, #0: seguimos, 1: Gana server, 2: Gana participante
        'score': g.score, #cantidad de rondas que el participante pudo continuar jugando.
        'game': gamer
    }

    return jsonify(data)
