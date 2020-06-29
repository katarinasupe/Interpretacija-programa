from pj import * 

class KEMIJA(enum.Enum):
    OTVORENA, ZATVORENA = '()'
    
    class BROJ(Token):
        def vrijednost(self, **mase):
            return int(self.sadržaj)
    
    class N(Token):
        def vrijednost(self, **mase):
            return mase[self.sadržaj]
    
    class ELEMENT(Token):
        def vrijednost(self, **mase):
            return self.sadržaj
    
def KEMIJA_lex(kod):
    lex = Tokenizer(kod)
    
    for znak in iter(lex.čitaj, ''):
        if znak.isspace():
            lex.zanemari()
        elif znak.isdigit():
            if znak != '0':
                lex.zvijezda(str.isdigit)
                
            yield lex.token(KEMIJA.BROJ)
        elif znak.isupper():
            lex.zvijezda(lambda slovo: slovo.islower() and slovo != 'n')
            
            yield lex.token(KEMIJA.ELEMENT)
        elif znak == 'n':
            yield lex.token(KEMIJA.N)
        else:
            yield lex.literal(KEMIJA)
            
class KEMIJA_parser(Parser):
    def formula(self):
        elementi = []
        
        while not self >> E.KRAJ:
            if self >= KEMIJA.ELEMENT:
                elementi.append(self.element())
            elif self >= KEMIJA.OTVORENA:
                elementi.append(self.spoj())
            else:
                raise self.greška()
                
        return Formula(elementi, Token(KEMIJA.BROJ, '1'))
            
    def spoj(self):
        elementi = []
        
        self.pročitaj(KEMIJA.OTVORENA)
        
        while not self >= KEMIJA.ZATVORENA:
            if self >= KEMIJA.ELEMENT:
                elementi.append(self.element())
            elif self >= KEMIJA.OTVORENA:
                elementi.append(self.spoj())
            else:
                raise self.greška()
        
        self.pročitaj(KEMIJA.ZATVORENA)
        
        if self >> KEMIJA.BROJ:
            broj = self.zadnji
        elif self >> KEMIJA.N:
            broj = self.zadnji
        else:
            broj = Token(KEMIJA.BROJ, '1')
            
        return Formula(elementi, broj)
            
    def element(self):
        ime = self.pročitaj(KEMIJA.ELEMENT)
        
        if self >> KEMIJA.BROJ:
            broj = self.zadnji
        else:
            broj = Token(KEMIJA.BROJ, '1')
            
        return Element(ime, broj)
        
    start = formula
            
class Formula(AST('elementi broj')):
    def vrijednost(self, **mase):
        masa = 0
        
        for elem in self.elementi:
            masa += elem.vrijednost(**mase)
            
        return masa * self.broj.vrijednost(**mase)
        
class Element(AST('element broj')):
    def vrijednost(self, **mase):
        return mase[self.element.vrijednost(*mase)] * self.broj.vrijednost(*mase)
        
# --------------------------------------------

kod = 'CH3(CH2)nCH3'

tokeni = list(KEMIJA_lex(kod))

fo = KEMIJA_parser.parsiraj(tokeni)

print(tokeni)
prikaz(fo, 10)

fo.vrijednost(C=12.01,H=1.008,n=2)
