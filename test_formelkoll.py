import unittest
from formelkoll import check_syntax

class TestMolekylSyntax(unittest.TestCase):

    def test_sample_1_correct_formulas(self):
        """Testar alla korrekta formler från Sample 1"""
        self.assertEqual(check_syntax("Na"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("H2O"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("Si(C3(COOH)2)4(H2O)7"), "Formeln är syntaktiskt korrekt")
        self.assertEqual(check_syntax("Na332"), "Formeln är syntaktiskt korrekt")

    def test_sample_2_incorrect_formulas(self):
        """Testar felaktiga formler från Sample 2 och deras felmeddelanden"""
        # De första tre felen från Sample 2
        self.assertEqual(check_syntax("C(Xx4)5"), "Okänd atom vid radslutet 4)5")
        self.assertEqual(check_syntax("C(OH4)C"), "Saknad siffra vid radslutet C")
        self.assertEqual(check_syntax("C(OH4C"), "Saknad högerparentes vid radslutet")
        
    def test_egen_fall(self):
        """Egna testfall föratt testa BNF-system"""
        #1)Korrekta men komplicerade strukturer
        self.assertEqual(check_syntax("(((H)2)3)4"), "Formeln är syntaktiskt korrekt")

        #2)Glömd siffra efter parentes
        #Enligt syntaxen MÅSTE en siffra komma efter ")" Vad händer om strängen tar slut där? Alltså inga fler tecken
        self.assertEqual(check_syntax("(H2O)"), "Saknad siffra vid radslutet")

        #3)Tomma parrentes
        #readmol förväntar sig en <group> men hittar ")"
        self.assertEqual(check_syntax("()2"), "Felaktig gruppstart vid radslutet )2")

if __name__ == '__main__':
    unittest.main()