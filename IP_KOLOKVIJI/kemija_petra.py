from pj import *

# prvo definiramo tipove tokena

class KF(enum.Enum):
	OTV, ZATV = '()'
	class ATOM(Token):
		def Mr(self, **atomi): # self UVIJEK TREBA BIT PRVI ARGUMENT KAD PISEMO KLASU U METODAMA
			return pogledaj(atomi, self)
	class BROJ(Token):
		def vrijednost(self, **_): #**_ nogli smo **atomi ali posto ih ne koristimo
			return int(self.sadržaj)
	class N(Token): # var N se moze pojavit samo neposredno nakon ) pa zelim to hendlat leksicki
		literal='n'
		def vrijednost(self, **atomi):
			return atomi['n']

def kf_lex(formula):
	lex=Tokenizer(formula)
	#ako vidim n želim provjerit prethodni znak
	prethodni = ''
	for znak in iter(lex.čitaj, ''):
		if (not prethodni or prethodni!=')') and znak =='n':
			raise lex.greska("nema ')' prije n!")
		elif znak.isdigit() and znak!=0:
			lex.zvijezda(str.isdigit) # procitaj sve znamenke
			yield lex.token(KF.BROJ)
		elif znak.isupper():
			idući=lex.čitaj()
			if not idući.islower():
				lex.vrati()
			yield lex.token(KF.ATOM)
		else:
			yield lex.literal(KF) # aako je bilo Cab b dode ode i onda baca gresku- neocekivan literal b
		prethodni = znak

# BKG
# formula -> formula skupina | skupina
# skupina -> ATOM | ATOM BROJ | OOTV formula OZATV (N|BROJ)? |  UOTV formula UZATV (N|BROJ)?

# AST
# Formula: skupine: [(Formula, broj|'n')] - dakle formula je lista skupina, a skupina je lista niza parova (formula, broj)

# bolje bi bilo gdje nije navedeno radit s 'nenavedeno' ko u nekom prije primjeru
# ovdje cemo mi ubasit jedinicu NIKAKO TO NE RADI lol
jedan=Token(KF.BROJ, '1')

class KFParser(Parser):
	def formula(self):
		skupine=[self.skupina()]
		while not self>={E.KRAJ, KF.ZATV}:
			skupine.append(self.skupina())
		return Formula(skupine)

	def skupina(self):
		if self >> KF.ATOM:
			atom=self.zadnji
			if self >> KF.BROJ:
				broj=self.zadnji
			else:
				broj=jedan
			return (atom, broj)
		else:
			self.pročitaj(KF.OTV)
			f=self.formula()
			self.pročitaj(KF.ZATV)
			if self >> {KF.N, KF.BROJ}:
				broj=self.zadnji
			else:
				broj=jedan
			return (f, broj)

	start=formula

# semantički analizator

class Formula(AST('skupine')):
	def Mr(self, **atomi): # ** za keyword arguments
		suma=0
		for skupina, broj in self.skupine:
			suma +=  skupina.Mr(**atomi)*broj.vrijednost(**atomi)
		return suma

if __name__=='__main__':
	formula='CH3(CH2)nCH3'
	tokeni=list(kf_lex(formula))
	p=KFParser.parsiraj(tokeni)
	print(tokeni, p, p.Mr(C=12.01, H=1.008, n=2), sep='\n\n')

	formula='CaH3(CaH2)nCaH3'
	tokeni=list(kf_lex(formula))
	p=KFParser.parsiraj(tokeni)
	print(tokeni, p, p.Mr(Ca=12.01, H=1.008, n=2), sep='\n\n')

	formula='CabH3(CabH2)nCabH3'
	tokeni=list(kf_lex(formula))
	p=KFParser.parsiraj(tokeni)
	print(tokeni, p, p.Mr(Cab=12.01, H=1.008, n=2), sep='\n\n')
