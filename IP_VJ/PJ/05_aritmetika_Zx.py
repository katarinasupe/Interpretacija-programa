"""Računanje polinomima u jednoj varijabli s cjelobrojnim koeficijentima.

Aritmetika cijelih brojeva je specijalni slučaj, kad se x ne pojavljuje.
Dozvoljeno je ispuštanje zvjezdice za množenje u slučajevima poput
  23x, xxxx, 2(3+1), (x+1)x, (x)(7) -- ali ne x3: to znači potenciranje!
Pokazuje se kako programirati jednostavne izuzetke od pravila BKG:
  konkretno, zabranjeni su izrazi poput (x+2)3, te (već leksički) 2 3.

Semantički analizator je napravljen u obliku prevoditelja (kompajlera) u
  klasu Polinom, čiji objekti podržavaju operacije prstena i lijep ispis.
"""


from pj import *
from backend import Polinom


class AZ(enum.Enum):
    PLUS, MINUS, PUTA, OTVORENA, ZATVORENA = '+-*()'
    class BROJ(Token):
        def vrijednost(self): return int(self.sadržaj)
        def prevedi(self): return Polinom.konstanta(self.vrijednost())
    class X(Token):
        literal = 'x'
        def vrijednost(self):
            raise NotImplementedError('Nepoznata vrijednost')
        def prevedi(self): return Polinom.x()


def az_lex(izraz):
    lex = Tokenizer(izraz)
    for znak in iter(lex.čitaj, ''):
        if znak.isdigit():
            lex.zvijezda(str.isdigit)
            yield lex.token(AZ.BROJ)
        else: yield lex.literal(AZ)


### Beskontekstna gramatika:
# izraz -> izraz PLUS član | izraz MINUS član | član
# član -> član PUTA faktor | faktor | MINUS član | član faktor *>vidi ↓ 
# faktor -> BROJ | X | X BROJ | OTVORENA izraz ZATVORENA


class AZParser(Parser):
    def izraz(self):
        trenutni = self.član()
        while True:
            if self >> AZ.PLUS: trenutni = Zbroj(trenutni, self.član())
            elif self >> AZ.MINUS:
                član = self.član()
                trenutni = Zbroj(trenutni, Suprotan(član))  # a-b:=a+(-b)
            else: break
        return trenutni

    def član(self):
        if self >> AZ.MINUS: return Suprotan(self.član())
        trenutni = self.faktor()
        while True:
            if self>>AZ.PUTA or self>={AZ.X,AZ.OTVORENA}:  # ali ne BROJ!
                trenutni = Umnožak(trenutni,self.faktor())
            else: return trenutni

    def faktor(self):
        if self >> AZ.BROJ: return self.zadnji
        elif self >> AZ.X:
            x = self.zadnji  # spremimo x jer donji >> uništi self.zadnji
            if self >> AZ.BROJ: return Xna(self.zadnji)
            else: return x
        elif self >> AZ.OTVORENA:
            u_zagradi = self.izraz()
            self.pročitaj(AZ.ZATVORENA)
            return u_zagradi
        else: raise self.greška()

    start = izraz


class Zbroj(AST('lijevo desno')):
    def prevedi(self):
        l, d = self.lijevo.prevedi(), self.desno.prevedi()
        return l + d
    
class Umnožak(AST('lijevo desno')):
    def prevedi(self):
        l, d = self.lijevo.prevedi(), self.desno.prevedi()
        return l * d

class Suprotan(AST('od')):
    def prevedi(self): return -self.od.prevedi()
    
class Xna(AST('eksponent')):
    def prevedi(self): return Polinom.x(self.eksponent.vrijednost())


def izračunaj(zadatak):
    print(zadatak, '=', AZParser.parsiraj(az_lex(zadatak)).prevedi())

if __name__ == '__main__':
    izračunaj('(5+2*8-3)(3-1)-(-4+2*19)')
    izračunaj('x-2+5x-(7x-5)')
    izračunaj('(((x-2)x+4)x-8)x+7')
    izračunaj('xx-2x+3')
    izračunaj('(x+1)' * 7)
    izračunaj('-'.join(['(x2-2x3-(7x+5))'] * 2))
