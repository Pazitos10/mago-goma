from BagWords import BagWords, Unsyllable, WordUsed, InvalidRule
import numpy as np

OK = 0
ERROR_WORD_USED = 1
ERROR_INVALID_RULE = 2
ERROR_UNSYLLABLE = 3
BULLSHIT = 4
ERROR_NOT_WORD = 5
USER = 2
CPU = 1

np.random.seed(17)


class State():
    
    def __init__(self, game, words, bw, gamer, score):
        self.game = game
        self.bw = bw
        self.words = words
        self.gamer = gamer
        self.score = score

    def run(self, word=None):
        pass


class Start(State):
    
    def bullshit(self):
        self.game.state = Bullshit(self.game, self.words, self.bw, self.gamer, self.score)

    
    def run(self, word=None):
        if word == None:
            answer = np.array(self.words[np.random.choice(list(self.words.keys()))])
            word = np.random.choice(answer)
            self.bw.add_word(word)
            self.gamer = USER
            return OK, word, OK, self.score
                
        self.bw.add_word(word)
        self.gamer = CPU
        self.game.state = Continue(self.game, self.words, self.bw, self.gamer, self.score)
        
        return self.game.state.run(word)


class Continue(State):
    
    def bullshit(self):
        self.game.state = Bullshit(self.game, self.words, self.bw, self.gamer, self.score)

    def run(self, word=None):
        if self.gamer == USER:
            self.bw.add_word(word)
            self.gamer = CPU
            answer = np.array(self.words[self.bw.last_syllable_word])
            word = np.random.choice(answer)
            self.bw.add_word(word)
            self.gamer = USER

        else:
            answer = np.array(self.words[self.bw.last_syllable_word])
            word = np.random.choice(answer)
            self.bw.add_word(word)
            self.gamer = USER
        
        self.score += 1

        return OK, word, OK, self.score

class Bullshit(State):

    def bullshit(self):
        self.run("Perdí :/")

    def run(self, word=None):
        if self.gamer == CPU:
            self.gamer = USER
            self.bw.add_word(word)
            #self.gamer = USER
        else:
            try:
                self.gamer = CPU
                answer = np.array(self.words[self.bw.last_syllable_word])
                word = np.random.choice(answer)
                self.bw.add_word(word)
                
            except Exception as e:
                self.gamer = CPU
                self.bw.add_word("Perdi") 

        return self.gamer, word, BULLSHIT, self.score




class Game():
    
    def __init__(self, dataset_txt):
        self.score = 0
        self.bw = BagWords()
        self.words = self.load_dictionary(dataset_txt)
        self.gamer = CPU
        self.state = Start(self, self.words, self.bw, self.gamer, self.score)
        

    def load_dictionary(self, dataset_txt):
        
        with open(dataset_txt) as f:
            es_words = f.read().splitlines()
        dic = self.preprocess_dictionary(es_words)
        return dic


    def preprocess_dictionary(self, es_words):
        """Crea un diccionario donde las claves son las primeras silabas de las palabras y
            los valores son las listas de palabras que comienzan con esa silaba"""
        #agrupar palabras por la primera silaba para agilizar busqueda
        dic = {}
        for w in es_words:
            try:
                first, _ = self.bw._separate_into_syllables(w)
                if not first in dic.keys():
                    dic.update({first: [w]})
                else:
                    dic[first].append(w)
            except Unsyllable:
                continue
        return dic


    def bullshit(self):
        self.state.bullshit()
    
    def run(self, word=None):
        
        try:
            self.gamer, word, code, self.score = self.state.run(word)
            return self.gamer, word, code
        
        except KeyError:
            #desconfio por parte del CPU
            self.bullshit()
            return self.state.gamer, word, BULLSHIT

        except Unsyllable:
            #print("monosilaba")
            return self.state.gamer, word, ERROR_UNSYLLABLE
        except WordUsed:
            #print("palabra usada")
            return self.state.gamer, word, ERROR_WORD_USED
        except InvalidRule:
            #print("No cumple con la regla")
            return self.state.gamer, word, ERROR_INVALID_RULE
       





