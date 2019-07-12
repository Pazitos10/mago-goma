import unittest
from BagWords import BagWords, Unsyllable, InvalidRule, WordUsed
from Game import Game

class TestGame(unittest.TestCase):
    
    def __init__(self, test):
        unittest.TestCase.__init__(self, test)
        self.bw = BagWords()
    
    def test_run(self):
        words = []
        g = Game("palabras_espanol.txt")
        p = g.run()
        words.append(p)
        words.append("consejo")
        p = g.run("consejo")
        words.append(p)
        words.append("dadme")
        p = g.run("dadme")
        words.append(p)
        words.append("ciobar")
        p = g.run("ciobar")
        words.append(p)
        words.append("zalsa")
        p = g.run("zalsa")
        words.append(p)
        self.assertEqual(g.bw.words_normalized, words)
        self.assertEqual(g.score, 4)
        g.run("balde")
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
