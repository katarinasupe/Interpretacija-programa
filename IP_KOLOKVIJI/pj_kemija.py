from pj import *

class KS(enum.Enum):
    UOTV, UZATV, OOTV, OZATV = '[]()'
    class N(Token):
        literal = 'n'
        def vrijednost(self, **atomi):
            return atomi['n']
    class BROJ(Token):
        def vrijednost(self, **_): 
            return int(self.sadržaj) #**_ underscore kako necemo koristiti atomi
    class ATOM(Token):
        def Mr(self, **atomi):
            return pogledaj(atomi, self)


def ks_lex(kod):
    lex = Tokenizer(kod)
    prethodni = ''
    for znak in iter(lex.čitaj,''):
        if (not prethodni or (prethodni != ')' and prethodni !=']')) and znak == 'n':
            raise lex.greška("nema zatvorene zagrade prije n!")
        elif znak.isspace(): lex.greška('Nisu dozvoljeni razmaci.')
        #elif znak == 'n':
        #    yield lex.token(KS.N)
        elif znak.isdigit():
            lex.zvijezda(str.isdigit)
            trenutni_broj = lex.sadržaj
            if trenutni_broj != '0' or trenutni_broj[0] != '0': #ne zelim samo 0 (pozitivni) niti 01, 002 ili sl.
                yield lex.token(KS.BROJ)
            else: raise lex.greška('Broj može biti samo pozitivan.')
        elif znak.isupper():
            iduci_znak = lex.čitaj()
            if not iduci_znak.islower():
                lex.vrati()
            yield lex.token(KS.ATOM)
        else: 
            yield lex.literal(KS)
        prethodni = znak


### BESKONTEKSTNA GRAMATIKA
# formula -> molekula molekule 
# molekule -> '' | molekula molekule | molekula UOTV molekule UZATV (BROJ | N)
# molekula -> atomi | OOTV atomi OZATV (BROJ | N)
# atomi -> ATOM | atomi (BROJ)?


# HORVAT
# formula -> formula skupina | skupina
# skupina -> UOTV formula UZATV (N|BROJ)? | OOTV formula OZATV (N|BROJ)? | ATOM (BROJ)?

# AST
# Formula: skupine: [(Formula, broj|'n')]
jedan = Token(KS.BROJ, '1')

class KSParser(Parser):
    def formula(self):
        skupine = [self.skupina()]
        while not self >= {E.KRAJ, KS.OZATV, KS.UZATV}:
            skupine.append(self.skupina())
        return Formula(skupine)

    def skupina(self):

        if self >> KS.ATOM:
            atom = self.zadnji
            if self >> KS.BROJ:
                broj = self.zadnji
            else:
                broj = jedan
            return (atom, broj)

        elif self >> KS.UOTV:
            formula = self.formula()
            self.pročitaj(KS.UZATV)
            if self >> {KS.N, KS.BROJ}:
                broj = self.zadnji
            else: 
                broj = jedan
            return (formula, broj)

        elif self >> KS.OOTV:
            formula = self.formula()
            self.pročitaj(KS.OZATV)
            if self >> {KS.N, KS.BROJ}:
                broj = self.zadnji
            else: 
                broj = jedan
            return (formula, broj)

    start = formula


#semantički analizator 

class Formula(AST('skupine')):
    def Mr(self, **atomi): #molna masa spoja
        suma = 0
        for skupina, broj in self.skupine:
            suma += skupina.Mr(**atomi) * broj.vrijednost(**atomi)
        return suma




if __name__ =='__main__':
    formula = '[CH3(CH2)]nCH3'
    tokeni = list(ks_lex(formula))
    p = KSParser.parsiraj(tokeni)
    print(*tokeni) #otpakiraj (bez [ ])
    print()
    print(p)
    print()
    print(p.Mr(C=12.01, H = 1.008, n=2))