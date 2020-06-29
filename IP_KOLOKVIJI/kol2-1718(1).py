from pj import *

## Tokeni
class LOOP(enum.Enum):
    ZAREZ, ZVJ, OOTV, OZATV = ',*()'
    INC1, DEC1 = 'INC', 'DEC'
    INC2, DEC2 = 'inc', 'dec'

    class RJ(Token):
        def vrijednost(self):
            return int(self.sadržaj[1:])


## Lekser - leksička analiza
def loop_lex(program):
    lex = Tokenizer(program)
    for znak in iter(lex.čitaj, ''):
        if znak.isspace(): lex.token(E.PRAZNO)
        elif znak == 'R':
            sljedeći = lex.čitaj()
            if not sljedeći.isdigit(): raise lex.greška('Nakon R mora slijediti broj')
            if sljedeći != '0': lex.zvijezda( str.isdigit )
            yield lex.token(LOOP.RJ)
        elif znak == 'I':
            lex.pročitaj('N')
            lex.pročitaj('C')
            yield lex.token(LOOP.INC1)
        elif znak == 'D':
            lex.pročitaj('E')
            lex.pročitaj('C')
            yield lex.token(LOOP.DEC1)
        elif znak == 'i':
            lex.pročitaj('n')
            lex.pročitaj('c')
            yield lex.token(LOOP.INC2)
        elif znak == 'd':
            lex.pročitaj('e')
            lex.pročitaj('c')
            yield lex.token(LOOP.DEC2)
        else: yield lex.literal(LOOP)


## BKG
# program -> naredba (, naredba)*
# naredba -> RJ ZVJ OOTV program OZATV | RJ ZVJ naredba | ZVJ RJ OOTV program OZATV | ZVJ RJ naredba | izraz
# izraz -> INC RJ | DEC RJ


## Parser - sintaksna analiza
class LOOPParser(Parser):
    def program(self):
        naredbe = []
        naredbe.append( self.naredba() )

        while self >> LOOP.ZAREZ:
            naredbe.append( self.naredba() )

        return Program(naredbe)

    def naredba(self):
        if self >> LOOP.RJ:
            registar = self.zadnji
            self.pročitaj(LOOP.ZVJ)
            if self >> LOOP.OOTV:
                naredbica = self.program()
                self.pročitaj(LOOP.OZATV)
            else:
                naredbica = self.naredba()
            return OgraničenaPetlja(registar, naredbica)

        elif self >> LOOP.ZVJ:
            registar = self.pročitaj(LOOP.RJ)
            if self >> LOOP.OOTV:
                naredbica = self.program()
                self.pročitaj(LOOP.OZATV)
            else:
                naredbica = self.naredba()
            return NeograničenaPetlja(registar, naredbica)

        else: return self.izraz()

    def izraz(self):
        if self >> {LOOP.INC1, LOOP.INC2}:
            registar = self.pročitaj(LOOP.RJ)
            return Inkrement(registar)
        elif self >> {LOOP.DEC1, LOOP.DEC2}:
            registar = self.pročitaj(LOOP.RJ)
            return Dekrement(registar)


    start = program


# Semantička analiza
max = -1

class Program(AST('naredbe')):
    def maxreg(self):
        global max
        for naredba in self.naredbe:
            naredba.maxreg()

        return max

    def izvrši(self,mem):
        for naredba in self.naredbe:
            naredba.izvrši(mem)


class OgraničenaPetlja(AST('registar naredbica')):
    def maxreg(self):
        global max
        broj = self.registar.vrijednost()
        if broj > max: max = broj

        self.naredbica.maxreg()

    def izvrši(self,mem):
        broj = mem[self.registar]
        for i in range(broj):
            self.naredbica.izvrši(mem)


class NeograničenaPetlja(AST('registar naredbica')):
    def maxreg(self):
        global max
        broj = self.registar.vrijednost()
        if broj > max: max = broj

        self.naredbica.maxreg()

    def izvrši(self,mem):
        while mem[self.registar]:
            self.naredbica.izvrši(mem)


class Inkrement(AST('registar')):
    def maxreg(self):
        global max
        broj = self.registar.vrijednost()
        if broj > max: max = broj

    def izvrši(self,mem):
        mem[self.registar] += 1


class Dekrement(AST('registar')):
    def maxreg(self):
        global max
        broj = self.registar.vrijednost()
        if broj > max: max = broj

    def izvrši(self,mem):
        mem[self.registar] -= 1


## Emulator
def run(lista, program):

    ## Resetiraj RAM stroj
    mem = {}

    ## Spremi registre i njihove vrijednosti iz liste u rječnik mem
    for i in range(len(lista)):
        vrijednost = 'R' + str(i)
        registar = Token(LOOP.RJ, vrijednost)
        mem[registar] = lista[i]

    ## Izvrši program L
    program.izvrši(mem)

    ## Vrati broj koji se nalazi u R0
    return mem[ Token(LOOP.RJ, 'R0') ]


if __name__ == '__main__':

    ulaz = """R2*DECR2,R3*(INCR2,DECR3)"""

    print("\n************** ULAZ: **************")
    print(ulaz)

    print("\n\n************** TOKENI: **************")
    tokeni = list(loop_lex(ulaz))
    print(*tokeni)

    print("\n\n************** PARSIRANJE: **************")
    stablo = LOOPParser.parsiraj(loop_lex(ulaz))
    print(stablo)

    print("\n\n************** MAXREG: **************")
    parser = LOOPParser.parsiraj(tokeni)
    print( parser.maxreg() )

    print("\n\n************** EMULATOR: **************")
    parser = LOOPParser.parsiraj(tokeni)
    lista = [1,0,5,6,0]
    print( run(lista, parser) )
