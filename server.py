from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home(name=None):
    return render_template('game.html', name=name)

@app.route('/procesar/<palabra>')
def procesar_palabra(palabra=None):
    pass