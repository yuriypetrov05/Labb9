import sys

"""Precis som i labb 8 så kommer koden fråga  "Vad är nästa tecken?" och "stämmer det med regeln?"""

ATOMER = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Fl Lv".split()

class Syntaxfel(Exception):
    pass

class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

class LinkedQueue:
    def __init__(self):
        self.first = None
        self.last = None

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.first = new_node
        else:
            self.last.next = new_node
        self.last = new_node

    def dequeue(self):
        # Ta ut och returnera nästa tecken
        if self.is_empty():
            return "" # Returnerar tom sträng om kön är tom
        value = self.first.value
        self.first = self.first.next
        if self.first is None:
            self.last = None
        return value

    def is_empty(self):
        return self.first is None

    def peek(self):
        # Titta på första värdet i kön utan att plocka ut det
        if self.is_empty():
            return ""
        return self.first.value

    def get_rest(self):
        # Plockar ut allt som är kvar i kön och bygger en sträng
        rest = ""
        while not self.is_empty():
            rest += self.dequeue()
        return rest


# --- REKURSIV MEDÅKNING (TOP-DOWN) ---

def readformel(q):
    """<formel> ::= <mol> \n"""
    readmol(q)

    # Om inmatning är inte slut när molekylen färdigläst
    # då är nästa tecken en ogiltig gruppstart
    if not q.is_empty():
        raise Syntaxfel("Felaktig gruppstart")

def readmol(q):
    # På samma sätt ska följa nya regeln
    """ <mol> ::= <group> | <group><mol> """
    readgroup(q)

    # Fortsätt läsa nästa grupp om vi inte har nått slutet på strängen
    # en högerparantes betyder att vi ska backa ur den.
    if q.peek() != "" and q.peek() != ")":
        readmol(q)

def readgroup(q):
    """ <group> ::= <atom> | <atom><num> | (<mol>) <num> """
    char = q.peek()

    if char == "(":
        q.dequeue()  #ta bort "(" från kön
        readmol(q)   #Läs innehållet inuti parentes

        if q.peek() != ")":
            raise Syntaxfel("Saknad högerparentes")
        q.dequeue()

        readnum(q)  # Efter parentes måste det enligt BNF-syntax komma en siffra

    elif char.isalpha(): # Om det är en bokstav (oavsett stor/liten)
        readatom(q)

        # Om det råkar komma en siffra direkt efter atomen, läs in den.
        if q.peek().isdigit():
            readnum(q)

    else:
        # Om vi förväntar oss en grupp men får något annat
        raise Syntaxfel("Felaktig gruppstart")

def readatom(q):
    """Eftersom vi måste kolla om atomen finns i ATOMER-listan så bygger jag atomen inuti readatom
    och sedan kontrollerar det. Alltså jag gör det på en gång"""
    """ <atom>  ::= <LETTER> | <LETTER><letter> """
    atom_namn = ""

    # 1) Kolla första tecken (Som måste vara stor bokstav)
    char1 = q.peek()
    if char1.isupper():
        atom_namn += q.dequeue()
    else:
        # Detta ska fånga "Saknad stor bokstav..."
        raise Syntaxfel("Saknad stor bokstav")

    # 2) Kolla andra tecken (kan va liten bokstav)
    char2 = q.peek()
    if char2.islower():
        atom_namn += q.dequeue()

    # 3) Kontrollera med periodiska systemet.
    if atom_namn not in ATOMER:
        raise Syntaxfel("Okänd atom")

def readnum(q): 
    # Kräver att nästa tecken inte är "0"
    """ <num> ::= 2 | 3 | 4 | ... """
    char = q.peek()

    if char == "" or not char.isdigit():
        raise Syntaxfel("Saknad siffra")

    if char == "0":
        q.dequeue()
        raise Syntaxfel("För litet tal")

    num_str = ""
    while q.peek().isdigit():
        num_str += q.dequeue()
        
    #Verifiera att det är korrekt längd/värde.
    if int(num_str) < 2:
        raise Syntaxfel("För litet tal")


#---HUVUDPROGRAM OCH KÖRNING---

def check_syntax(formel):
    #Skapa instans av LinkedQueue och fyll den med tecken
    q = LinkedQueue()
    for char in formel:
        q.enqueue(char)

    try:
        readformel(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as e:
        # .strip() tar bort osynliga mellanslag i slutet av sträng
        return f"{str(e)} vid radslutet {q.get_rest()}".strip()

def main():
    #Läser rad för rad från standard input
    for line in sys.stdin:
        # Ta bort eventuella nyradstecken och mellanslag i slutet av raden
        formel = line.strip()

        #Avbryt om man hittar "#"
        if formel == "#":
            break
            
        #Kör syntaxkontroll.
        resultat = check_syntax(formel)
        print(resultat)

if __name__ == '__main__':
    main()