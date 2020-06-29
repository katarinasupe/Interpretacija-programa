#Liste

from pj import *

###Tokeni
class L(enum.Enum):
    LISTA, PRAZNA, UBACI='LISTA', 'PRAZNA', 'UBACI'
    IZBACI, DOHVATI, KOLIKO='IZBACI', 'DOHVATI', 'KOLIKO'

    class IME(Token): #sadrzaj nije uvijek isti
        pass
#pise da se u listi nalaze cijeli brojevi,pa imas i negativne
    class BROJ(Token):
        def vrijednost(self):
            return int(self.sadržaj)

    class MINUSBROJ(Token):
        def vrijednost(self):
            return int(self.sadržaj)




###Pomocne funkcije za lexer
def isdigit_(znak):
    """
    Vraca True ako je broj izmedu 1-9,inace False
    """
    if znak.isdigit():
        broj=int(znak)
        if 1<=broj<=9:
            return True
        else:
            return False
        
###Lexer
def l_lex(program):
    lex=Tokenizer(program)
    for znak in iter(lex.čitaj,''):
        if znak.isspace(): lex.token(E.PRAZNO)
        elif znak == 'L':
            znakic=lex.pogledaj()
            if(isdigit_(znakic)): #mogli tu samo stavit '1'<=lex.
                lex.čitaj()
                yield lex.token(L.IME)
            else:
                lex.zvijezda(str.isalpha)
                yield lex.literal(L)
        elif znak.isdigit(): #pazi da nakon znak.isdigit() stavis ove zagrade!
            lex.zvijezda(str.isdigit)
            yield lex.token(L.BROJ)
        elif znak=='-':
            broj=lex.čitaj()
            if not broj.isdigit():
               lex.greška('očekivan broj')
            lex.zvijezda(str.isdigit)
            yield lex.token(L.MINUSBROJ)

        else:
            lex.zvijezda(str.isalnum)
            yield lex.literal(L)
        

###Beskontekstna gramatika
# start -> naredba start | naredba
# naredba -> lista | prazna | izbaci | ubaci | dohvati | koliko
# lista -> LISTA IME
# prazna -> PRAZNA IME
# ubaci -> UBACI IME broj BROJ
# izbaci -> IZBACI IME BROJ
# dohvati -> DOHVATI IME BROJ
# koliko -> KOLIKO IME
# broj -> BROJ | MINUSBROJ

###Parser
class LParser(Parser):
    def start(self):
        naredbe=[]
        while not self >> E.KRAJ:
            naredbe.append(self.naredba())
        return Program(naredbe)
    
    def broj(self):
        if self >> L.BROJ:
            return self.zadnji
        elif self >> L.MINUSBROJ:
            return self.zadnji 

    def naredba(self):
        if self >> L.LISTA:
            ime_liste=self.pročitaj(L.IME)
            return Lista(ime_liste)
        elif self >> L.PRAZNA:
            ime_liste=self.pročitaj(L.IME)
            return Prazna(ime_liste)
        elif self >> L.UBACI:
            ime_liste=self.pročitaj(L.IME)
            broj_ubaci=self.broj()
            broj=self.pročitaj(L.BROJ)
            return Ubaci(ime_liste,broj_ubaci,broj)
        elif self >> L.IZBACI:
            ime_liste=self.pročitaj(L.IME)
            broj=self.pročitaj(L.BROJ)
            return Izbaci(ime_liste,broj)
        elif self >> L.DOHVATI:
            ime_liste=self.pročitaj(L.IME)
            broj=self.pročitaj(L.BROJ)
            return Dohvati(ime_liste,broj)
        elif self >> L.KOLIKO:
            ime_liste=self.pročitaj(L.IME)
            return Koliko(ime_liste)
        else:
            self.greška()

###AST
class Program(AST('naredbe')):
    mem={}
    def pozovi(self):       
        try:
            for naredba in self.naredbe:
                naredba.izvrši(self.mem) #ako ces mem deklarirat izvan onda moras stavit ovako
                #self.mem...jer pozivas kao bas njegov,a nisi ga dobila u ovo pozovi!!!
        except Povratak as exc: return exc.povratna_vrijednost

class Lista(AST('ime')): #ti s ovim ime dobijes taj token koji ima svoje ovo kao ime,sadrzaj i poziciju
    def izvrši(self,mem):#pa svugdi di ga koristis moras pristupat njegovom sadrzaju
        mem[self.ime.sadržaj]=[]
        print("Deklarirao listu.")

class Prazna(AST('ime')):
    def izvrši(self,mem):
        if mem[self.ime.sadržaj]:
            print("Nije prazna lista")
        else:
            print("Prazna lista")


class Ubaci(AST('ime broj_ubaci broj')):
    def izvrši(self,mem):
        if int(self.broj.sadržaj)<=len(mem[self.ime.sadržaj]):
            mem[self.ime.sadržaj].insert(int(self.broj.sadržaj),int(self.broj_ubaci.sadržaj))
        else:
            self.broj.greška("Prevelik index")

class Izbaci(AST('ime broj')):
    def izvrši(self,mem):
        if int(self.broj.sadržaj)<=len(mem):
            del mem[self.ime.sadržaj][int(self.broj.sadržaj)]
        else:
            self.broj.greška("Prevelik index")

class Dohvati(AST('ime broj')):
    def izvrši(self,mem):
        if int(self.broj.sadržaj)<=len(mem):
            return mem[self.ime.sadržaj][int(self.broj.sadržaj)]
        else:
            self.broj.greška("Prevelik index")


class Koliko(AST('ime')):
    def izvrši(self,mem):
        return len(mem[self.ime.sadržaj])
     
class Povratak(Exception):
    @property
    def povratna_vrijednost(self): return self.args[0]    
        
        
        
        
        


#testiranje
if __name__=='__main__':
    ulaz = '''\
                LISTA L5 PRAZNA L5
                LISTA L3 UBACI L3 45 0
                DOHVATI L3 0
                KOLIKO L3
                KOLIKO L5
           '''
    print(ulaz)

    tokeni=list(l_lex(ulaz))
    print(*tokeni)
    p=LParser.parsiraj(tokeni)
    print(*p)
    p.pozovi()
    print(*p)
        
