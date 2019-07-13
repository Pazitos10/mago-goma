import unittest
from BagWords import BagWords, Unsyllable, InvalidRule, WordUsed
from Game import CPU, USER, ERROR_INVALID_RULE, ERROR_WORD_USED, ERROR_UNSYLLABLE, OK, BULLSHIT
from Game import Game
import numpy as np

class TestGame(unittest.TestCase):
    
    def __init__(self, test):
        unittest.TestCase.__init__(self, test)
        self.bw = BagWords()
    
    def test_add_word(self):
        self.bw.add_word("Nacer")
        self.assertEqual(self.bw.words, ["Nacer"])
        self.bw.add_word("Cercano")
        self.assertEqual(self.bw.words, ["Nacer", "Cercano"])

        with self.assertRaises(InvalidRule):
            self.bw.add_word("Normal")
        
        with self.assertRaises(WordUsed):
                self.bw.add_word("Nacer")

    def test_normalize(self):
        self.assertEqual(self.bw._normalize("coMputAción"), "computacion")
        self.assertEqual(self.bw._normalize("árBol"), "arbol")
        self.assertEqual(self.bw._normalize("únicO"), "unico")
        self.assertEqual(self.bw._normalize("joSé"), "jose")
    
    
    def test_separate_into_syllables(self):
        self.assertEqual(self.bw._separate_into_syllables("cascada"), ('cas', 'da'))
        with self.assertRaises(Unsyllable):
            self.bw._separate_into_syllables("no")

    def test_is_unsyllable(self):
        self.assertFalse(self.bw._is_unsyllable('casa'))
        self.assertTrue(self.bw._is_unsyllable('no'))

    def test_run(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        #words = ["consejo", "dadme", "ciobar", "zalsa"]
        words = ["diamante", "llamame", "temor"]
        gamer, word, error = g.run()
        for w in words:
            gamer, word, error = g.run(w)
            self.assertEqual(gamer, 0)
        
        #self.assertEqual(g.bw.words, ['Helicón', 'consejo', 'jocundidad', 'dadme', 'meretricio', 'ciobar', 'barzal', 'zalsa', 'sayón'])
        self.assertEqual(g.bw.words,['salvaguardia',
                                     'diamante',
                                     'tetilla',
                                     'llamame',
                                     'meritoriamente',
                                     'temor',
                                     'morgaño'])
        self.assertEqual(g.score, 3)
    
    
    def test_user(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        gamer, word, error = g.run("hola")
        gamer, word, error = g.run("dominar")
        gamer, word, error = g.run("dominio")
        self.assertEqual(error, OK)
    
    def test_user_win(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        gamer, word, error = g.run("hola")
        gamer, word, error = g.run("dominar")
        gamer, word, error = g.run("dominio")
        gamer, word, error = g.run("torre")
        self.assertEqual(error, BULLSHIT)
        gamer, word, error = g.run("rremar")
        self.assertEqual(gamer, USER)
        self.assertEqual(error, OK)
        print(word)
    
    
    def test_run_error_invalid_rule(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        gamer, word, error = g.run()
        gamer, word, error = g.run("balde")
        self.assertEqual(gamer, USER)
        self.assertEqual(error, ERROR_INVALID_RULE)
    
    def test_run_error_word_used(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        gamer, word, error = g.run()
        gamer, word, error = g.run("salvaguardia")
        self.assertEqual(gamer, USER)
        self.assertEqual(error, ERROR_WORD_USED)
    
    def test_run_error_unsyllable(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        gamer, word, error = g.run()
        gamer, word, error = g.run("Si")
        self.assertEqual(gamer, USER)
        self.assertEqual(error, ERROR_UNSYLLABLE)

    def test_bullshit(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        gamer, word, error = g.run("hola")
        gamer, word, error = g.run("dominar")
        g.bullshit()
        gamer, word, error = g.run(word)
        self.assertEqual(gamer, CPU)
        self.assertEqual(error, OK)
    


if __name__ == '__main__':
    unittest.main()
