import unittest
from BagWords import BagWords, Unsyllable, InvalidRule, WordUsed
from Game import Game
import numpy as np

class TestGame(unittest.TestCase):
    
    def __init__(self, test):
        unittest.TestCase.__init__(self, test)
        self.bw = BagWords()
    
    def test_run(self):
        np.random.seed(17)
        g = Game("test_palabras_espanol.txt")
        c, p = g.run()
        self.assertEqual(c, 0)
        c, p = g.run("consejo")
        self.assertEqual(c, 0)
        c, p = g.run("dadme")
        self.assertEqual(c, 0)
        c, p = g.run("ciobar")
        self.assertEqual(c, 0)
        c, p = g.run("zalsa")
        self.assertEqual(c, 0)
        self.assertEqual(g.bw.words, ['Helicón', 'consejo', 'jocundidad', 'dadme', 'meretricio', 'ciobar', 'barzal', 'zalsa', 'sayón'])
        self.assertEqual(g.score, 4)
        c, p = g.run("balde")
        
        self.assertEqual(g.score, 4)
        """with self.assertRaises(InvalidRule):
            g.run("balde")"""

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
    


if __name__ == '__main__':
    unittest.main()
