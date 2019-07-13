from BagWords import BagWords, Unsyllable, WordUsed, InvalidRule
import numpy as np

OK = 0
ERROR_WORD_USED = 1
ERROR_INVALID_RULE = 2
ERROR_UNSYLLABLE = 3
ERROR_NOT_WORD = 4
USER = 2
CPU = 1

np.random.seed(17)




class Game():
    
    def __init__(self, dataset_txt):
        self.score = 0
        self.bw = BagWords()
        self.words = self.load_dictionary(dataset_txt)
        self.gamer = CPU
        

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

    def run(self, word=None):
        if word == None:
            answer = np.array(self.words[np.random.choice(list(self.words.keys()))])
            word = np.random.choice(answer)
            self.bw.add_word(word)
            return OK, word, OK

        try:
            self.gamer = USER
            self.bw.add_word(word)
            self.gamer = CPU
            answer = np.array(self.words[self.bw.last_syllable_word])
            word = np.random.choice(answer)
            self.bw.add_word(word)
            self.score += 1
            return OK, word, OK
        
        except KeyError:
            #desconfio por parte del CPU
            return self.gamer, word, ERROR_NOT_WORD

        except Unsyllable:
            #print("monosilaba")
            return self.gamer, word, ERROR_UNSYLLABLE
        except WordUsed:
            #print("palabra usada")
            return self.gamer, word, ERROR_WORD_USED
        except InvalidRule:
            #print("No cumple con la regla")
            return self.gamer, word, ERROR_INVALID_RULE








