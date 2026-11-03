import sys
"""Precis som i labb 8 så kommer koden fråga  "Vad är nästa tecken?" och "stämmer det med regeln?"""

ATOMER = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Fl Lv".split()

class Syntaxfel(Exception):
    pass

"""Eftersom vi måste kolla om atomen finns i ATOMER lista så bygger jag atomen inuti readatom
och sedan kontrollerar det. Alltså jag gör att på en gång"""
def readatom(q):
    """ <atom>  ::= <LETTER> | <LETTER><letter> """
    atom_namn = ""

    #1) Kolla första tecken (Som måste vara stor bokstav)
    char1 = q.peek()
    if char1.isupper():
        atom_namn += q.pop()
    else:
        #Detta ska fångar "Saknad stor bokstav..."
        raise Syntaxfel("Saknad stor bokstav")

    #2)Kolla andra tecken (kan va liten bokstav)
    char2 = q.peek()
    if char2.islower():
        atom_namn += q.pop()

    #3)Kontrollera  med periodiska systemet.
    if atom_namn not in ATOMER:
        raise Syntaxfel("Okänd atom")

def readnum(q): #Likt den från labb 8 fast utan dequeue
    """ <num> ::= 2 | 3 | 4 | ... """
    char = q.peek()

    if char == "" or not char.isdigit():
        raise Syntaxfel("Saknad siffra")

    if char == "0":
        q.pop()
        raise Syntaxfel("För litet tal")

    num_str = ""
    while q.peek().isdigit():
        num_str += q.pop()

    if int(num_str) <  2:
        raise Syntaxfel("För litet tal")

def readformel(q):
    """<formel> ::= <mol> \n"""
    readmol(q)

    #Om inmatning är inte slut när molekylen färdigläst
    #då är nästa tecken en ogiltig gruppstart
    if not q.is_empty():
        raise Syntaxfel("Felaktig gruppstart")

def readmol(q):
    #På samma sätt ska följa nya regeln
    """ <mol> ::= <group> | <group><mol> """
    readgroup(q)

    #Fortsätt läsa nästa grupp om vi inte har nått slutet på strängen
    #en högerparantes betyder att vi ska backa ur den.
    if q.peek() != "" and q.peek() != ")":
        readmol(q)

def readgroup(q):
    """ <group> ::= <atom> | <atom><num> | (<mol>) <num> """
    char = q.peek()

    if char == "(":
        q.pop()  #ta bort  "(" från kön
        readmol(q) #Läs innehålet inuti parentes

        if q.peek() != ")":
            raise Syntaxfel("Saknad högerparentes")
        q.pop()

        readnum(q)  #Efter parentes måste det följa enligt BNF-syntax komma en siffra

    elif char.isalpha(): #Om det är en bokstav (oavsett stor/liten)
        readatom(q)

        #Om det råkar komma en siffra direkt efter atomen,  läs in den.
        if q.peek().isdigit():
            readnum(q)

    else:
        #Om vi förväntar oss en grupp men får något annat
        raise Syntaxfel("Felaktig gruppstart")

def check_syntax(formel):
    q = FormelQueue(formel)

    try:
        readformel(q)
        return "Formeln är syntaktiskt korrekt"
    #.strip() tar bort osynliga mellanslag i slutet av sträng
    except Syntaxfel as e:
        return f"{str(e)} vid radslutet {q.get_rest()}".strip()


class FormelQueue:
    def __init__(self, formel_str):
        #Gör om strängen till en lsitaav tecken för enkel hantering
        self.queue = list(formel_str)

    def peek(self):
        #Tjuvtitta på nästa tecken utan att ta bort den
        #Returnera en tom sträng ifall kön är tom
        if self.is_empty():
            return ""
        return self.queue[0]

    def pop(self):
        #Ta bort och returnera nästa tecken.
        if self.is_empty():
            return "" #Returnera tom sträng om kön är tom
        return self.queue.pop(0)

    def is_empty(self):
        return len (self.queue) == 0

    def get_rest(self):
        #Här tar jag fram resten, kastar syntaxfel och ska skriva ut
        #"vid radslutet X" (menas tecken som är kvar när koden kraschades)
        return "".join(self.queue)


def main():
    #Läser rad för rad från standard input
    for line in sys.stdin:
        #Ta bort eventuella nyradstecken och mellanslag i slutet av raden
        formel = line.strip()

        #Avbryt om mman hittar "#"
        if formel =="#":
            break
        #Kör syntaxkontroll.
        resultat = check_syntax(formel)
        print(resultat)

if __name__ == '__main__':
    main()