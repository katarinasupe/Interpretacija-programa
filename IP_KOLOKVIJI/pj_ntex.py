from pj import *

class NT(enum.Enum):
    PLUS, VOTV, VZATV = '+', '{', '}'
    class MALA_VAR(Token):
        def širina(self, **_):
            return 11
    class VELIKA_VAR(Token):
        def širina(self, **_):
            return 12
    FRAC = '\\frac'

def nt_lex(kod):
    lex = Tokenizer(kod)
    for znak in iter(lex.čitaj, ''):
        if znak.isspace():
            lex.zanemari()
        elif znak == '\\':
            if lex.slijedi('f') and lex.slijedi('r') and lex.slijedi('a') and lex.slijedi('c'):
                yield lex.token(NT.FRAC)
        elif znak.isupper():
            yield lex.token(NT.VELIKA_VAR)
        elif znak.islower():
            yield lex.token(NT.MALA_VAR)
        else:
            yield lex.literal(NT)
        

# BKG
# izraz -> faktor | izraz faktor 
# faktor -> varijabla | varijabla PLUS varijabla | varijabla varijabla | FRAC varijabla varijabla
# varijabla -> MALA_VAR | VELIKA_VAR | VOTV faktor VZATV 

class NTParser(Parser):

    def izraz(self):
        faktori = [self.faktor()]
        while not self >= {E.KRAJ, NT.VZATV}: 
            faktori.append(self.faktor())
        return Izraz(faktori)
    
    def faktor(self):
        if self >> NT.FRAC:
            if self >> NT.VOTV:
                brojnik = self.faktor()
                self.pročitaj(NT.VZATV)
                if self >> NT.VOTV:
                    nazivnik = self.faktor()
                    self.pročitaj(NT.VZATV)
                else:
                    nazivnik = self.pročitaj(NT.MALA_VAR, NT.VELIKA_VAR)
            else:
                brojnik = self.pročitaj(NT.MALA_VAR, NT.VELIKA_VAR)
                if self >> NT.VOTV:
                    nazivnik = self.faktor()
                    self.pročitaj(NT.VZATV)
                else:
                    nazivnik = self.pročitaj(NT.MALA_VAR, NT.VELIKA_VAR)
            return Razlomak(brojnik, nazivnik)
        #varijabla, zbroj, umnozak
        else:
            if self >> NT.VOTV:
                vitice = True
                self.vrati()
            else:
                vitice = False
            var1 = self.varijabla()
            if self >> NT.PLUS:
                var2 = self.varijabla()
                return Zbroj(vitice, var1, var2)
            else:
                var2 = self.varijabla()
                return Umnožak(var1,var2)

    def varijabla(self):
        if self >> {NT.MALA_VAR, NT.VELIKA_VAR}:
            return self.zadnji
        if self >> NT.VOTV:
            faktor = self.faktor()
            self.pročitaj(NT.VZATV)
            return faktor

    start = izraz

class Izraz(AST('faktori')):
    def širina(self):
        suma = 0
        for faktor in self.faktori:
            suma += faktor.širina()
        return suma
class Razlomak(AST('brojnik, nazivnik')):
    def širina(self):
        return max( self.brojnik.širina(), self.nazivnik.širina() ) + 2 #1pt sa svake strane
class Zbroj(AST('vitice, var1, var2')):
    def širina(self):
        if self.vitice:
            return self.var1.širina() + self.var2.širina() + 12 + 4 + 4
        else:
            return self.var1.širina() + self.var2.širina() + 12 + 2 + 2 
class Umnožak(AST('var1, var2')):
    def širina(self):
        return self.var1.širina() + self.var2.širina()


if __name__ =='__main__':
    ulaz = '\\frac{ab}CH+d'
    tokeni = list(nt_lex(ulaz))
    print(*tokeni)

    fo = NTParser.parsiraj(tokeni)
    print(fo)

    print(fo.širina())