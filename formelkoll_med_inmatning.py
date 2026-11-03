# formelkollmedInmatning.py

ATOMER = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Fl Lv".split()

class Syntaxfel(Exception):
    pass

class FormelQueue:
    def __init__(self, formel_str):
        self.queue = list(formel_str)

    def peek(self):
        if self.is_empty():
            return ""
        return self.queue[0]

    def pop(self):
        if self.is_empty():
            return "" 
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def get_rest(self):
        return "".join(self.queue)

def readatom(q):
    """ <atom> ::= <LETTER> | <LETTER><letter> """
    atom_namn = ""
    
    char1 = q.peek()
    if char1.isupper():
        atom_namn += q.pop()
    else:
        raise Syntaxfel("Saknad stor bokstav")
        
    char2 = q.peek()
    if char2.islower():
        atom_namn += q.pop()
        
    if atom_namn not in ATOMER:
        raise Syntaxfel("Okänd atom")

def readnum(q):
    """ <num> ::= 2 | 3 | 4 | ... """
    char = q.peek()
    
    if char == "" or not char.isdigit():
        raise Syntaxfel("Saknad siffra")
        
    if char == '0':
        q.pop() 
        raise Syntaxfel("För litet tal")
        
    num_str = ""
    while q.peek().isdigit():
        num_str += q.pop()
        
    if int(num_str) < 2:
        raise Syntaxfel("För litet tal")

def readgroup(q):
    """ <group> ::= <atom> | <atom><num> | (<mol>) <num> """
    char = q.peek()
    
    if char == '(':
        q.pop()          
        readmol(q)       
        
        if q.peek() != ')':
            raise Syntaxfel("Saknad högerparentes")
        q.pop()          
        
        readnum(q)       
        
    elif char.isalpha(): 
        readatom(q)
        if q.peek().isdigit():
            readnum(q)
            
    else:
        raise Syntaxfel("Felaktig gruppstart")

def readmol(q):
    """ <mol> ::= <group> | <group><mol> """
    readgroup(q)
    
    if q.peek() != "" and q.peek() != ")":
        readmol(q)

def readformel(q):
    """ <formel> ::= <mol> \n """
    readmol(q)
    
    if not q.is_empty():
        raise Syntaxfel("Felaktig gruppstart")

def check_syntax(formel):
    q = FormelQueue(formel)
    try:
        readformel(q)
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as e:
        # .strip() rensar bort eventuellt onödigt mellanslag på slutet om kön är tom
        return f"{str(e)} vid radslutet {q.get_rest()}".strip()

def main():
    print("==================================================")
    print("Formelkollen (Manuell Testning) ")
    print("Skriv in en molekylformel och tryck Enter.")
    print("Skriv '#' för att avsluta programmet.")
    print("==================================================\n")
    
    while True:
        # Läs in inmatning från användaren (prompten väntar på text)
        formel = input("Mata in formel: ").strip()
        
        # Kolla om användaren vill avsluta
        if formel == "#":
            print("Avslutar programmet. Bra jobbat med labben!")
            break
            
        # Hoppa över ifall användaren bara råkade trycka Enter utan att skriva något
        if not formel:
            continue
            
        # Kör vår funktion och skriv ut resultatet
        resultat = check_syntax(formel)
        print(f"--> Svar: {resultat}\n")

if __name__ == '__main__':
    main()