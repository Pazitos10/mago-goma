from flask import Flask, render_template, jsonify
from Game import Game, ERROR_INVALID_RULE, ERROR_WORD_USED, ERROR_UNSYLLABLE, OK, BULLSHIT
import requests
import bs4
import json

app = Flask(__name__)

g = None


@app.route('/')
def home(name=None):
    global g
    g = Game("test_palabras_espanol.txt")
    _, word, _ = g.run()
    return render_template('game.html', name=name, word=word)

@app.route('/process/<word>', methods = ['POST'])   
def process_word(word=None):
    global g
    gamer, w, error = g.run(word)
    
    data = {
        'word': g.state.bw.last_word, #la palabra original (user)
        'answer': g.state.bw.actual_word, #La palabra respuesta o cadena vacía si no tiene respuesta (server).
        'state': error, #0: seguimos, 1: Gana server, 2: Gana participante
        'score': g.score, #cantidad de rondas que el participante pudo continuar jugando.
        'gamer': gamer,
        #'definition': get_definition(g.state.bw.actual_word)
    }

    return jsonify(data)

@app.route('/bullshit', methods = ['POST'])   
def bullshit():
    global g
    g.bullshit()
    gamer, w, error = g.run()

    data = {
        'word': g.state.bw.last_word, #la palabra original (user)
        'answer': g.state.bw.actual_word, #La palabra respuesta o cadena vacía si no tiene respuesta (server).
        'state': error, #0: seguimos, 1: Gana server, 2: Gana participante
        'score': g.score, #cantidad de rondas que el participante pudo continuar jugando.
        'gamer': gamer,
        #'definition': get_definition(g.state.bw.actual_word)
    }
    return jsonify(data)


@app.route('/definition/<word>', methods = ['GET'])
def get_definition(word):
    r = requests.get("https://es.thefreedictionary.com/{}".format(word))
    soup = bs4.BeautifulSoup(r.text, 'html')
    definition = word
    definition = soup.find("div", {'id': 'Definition'})
    return jsonify(definition.findChild().__str__())
