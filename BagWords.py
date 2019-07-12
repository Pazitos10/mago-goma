import pyphen
import numpy as np

class Unsyllable(Exception):
    """Excepcion lanzada cuando la palabra es monosilaba"""
    pass

class WordUsed(Exception):
    """Excepcion lanzada cuando se repite una palabra"""
    pass

class InvalidRule(Exception):
    """Excepcion lanzada cuando se repite una palabra"""
    pass


class BagWords():
    
    def __init__(self):
        self._dic = pyphen.Pyphen(lang='es')
        self.words = []
        self.words_normalized = []
        self.last_word = None
        self.last_syllable_word = None
        self.first_syllable_word = None
    
   
    def _valid_rule(self, _last_syllable_word):
        """ """
        if _last_syllable_word == None:
            return True
        return self.first_syllable_word == _last_syllable_word

    def add_word(self, word):
        """Valida si la ultima silaba de una palabra es la primera silaba de otra palabra"""
        normalized_word = self._normalize(word)
        _last_syllable_word = self.last_syllable_word
        self.first_syllable_word, self.last_syllable_word = self._separate_into_syllables(normalized_word)
        self.last_word = normalized_word
        
        if normalized_word in self.words_normalized:
            raise WordUsed
        
        if not self._valid_rule(_last_syllable_word):
            raise InvalidRule
        
        self.words_normalized.append(normalized_word)
        self.words.append(word)

    def _normalize(self, word):
        """Reemplaza los acentos en las vocales de las silabas por su equivalentes sin acentos"""
        dic_replace = {
            'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u',
        }
        
        for k, v in dic_replace.items():
            word = word.replace(k, v)
        return word.lower()

    def _separate_into_syllables(self, word):
        """Separa una palabra en silabas y devuelve la primera y ultima silibas de la misma o
        lanza la excepción Monosilaba si la palabra no se puede seguir dividiendo"""
        if not self._is_unsyllable(word):
            syllable = self._dic.inserted(word)
            f_syllable = syllable.split('-')[0]
            l_syllable = syllable.split('-')[-1]
            return f_syllable, l_syllable
        else:
            raise Unsyllable

    def _is_unsyllable(self, word):
        """Devuelve True si la palabra es monosilaba y False sino"""
        return not '-' in self._dic.inserted(word)



