import numpy as np
from flask import Flask, render_template, jsonify
from Game import Game, ERROR_INVALID_RULE, ERROR_WORD_USED, ERROR_UNSYLLABLE, OK, BULLSHIT


app = Flask(__name__)

@app.route('/')
def home(name=None):
    #np.random.seed(17)
    g = Game("test_palabras_espanol.txt")
    gamer, word, error = g.run()
    return render_template('game.html', name=name, word=word)

@app.route('/process/<word>', methods = ['POST'])   
def process_word(word=None):
    
    gamer, word, error = g.run()
    
    data = {
        'word': g.state.bw.last_word, #la palabra original
        'answer': word, #La palabra respuesta o cadena vacía si no tiene respuesta
        'state': error, #0: seguimos, 1: Gana server, 2: Gana participante
        'score': g.score(), #cantidad de rondas que el participante pudo continuar jugando.
        'game': gamer
    }

    return jsonify(data)
