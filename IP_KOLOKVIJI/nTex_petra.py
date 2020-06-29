from pj import *
import pprint


class TEX(enum.Enum):

	PLUS, VOTV, VZATV = '+{}'
	RAZLOMAK = '\\fract'

	class VSLOVO(Token):
		def širina(self, **_):
			return 12
	class MSLOVO(Token):
		def širina(self, **_):
			return 11


def TEX_lex(input):
	lex = Tokenizer(input)
	prethodni=''
	for znak in iter(lex.čitaj, ''):
		if znak.isspace():
			lex.zanemari()
		elif znak.isupper():
			yield lex.token(TEX.VSLOVO)
		elif znak.islower():
			yield lex.token(TEX.MSLOVO)
		elif znak=='\\':
			if lex.slijedi( 'f' ) and lex.slijedi( 'r' ) and lex.slijedi( 'a' ) and lex.slijedi( 'c' ):
				yield lex.token( TEX.RAZLOMAK )
		else: yield lex.literal(TEX)


# BKG
# izraz -> element | izraz element
# element -> član | član PLUS član | član član | RAZLOMAK član član
# član -> MSLOVO | VSLOVO | VOTV element VZATV



class TEX_Parser(Parser):

	def izraz(self):
		elementi = [self.element()] # članovi su lista koja sigurno ima jedan član
		while not self>={E.KRAJ, TEX.VZATV}:  # samo pogledamo zagradu i kraj
			elementi.append(self.element())
		#print('elementi:')
		#print(elementi)
		return Izraz(elementi)

	#ovdje ostavljamo sve zagrade da ih pročita član
	def element(self):

		if self >> TEX.RAZLOMAK:
			zagradeb = False
			zagraden = False
			if self >= TEX.VOTV:
				zagradeb = True
				brojnik = self.član()
			else:
				brojnik = self.pročitaj(TEX.MSLOVO, TEX.VSLOVO)

			if self >= TEX.VOTV:
				zagraden = True
				nazivnik = self.član()
			else:
				nazivnik = self.pročitaj(TEX.MSLOVO, TEX.VSLOVO)

			return Razlomak(zagradeb, zagraden, brojnik, nazivnik)

		else:
			if self >= {TEX.VOTV}:
				zagrada = True
			else: zagrada = False
			prvi = self.član()

			if self >> TEX.PLUS:
				if self >= {TEX.VOTV}:
					zagrada = True
				return Zbroj(zagrada, prvi, self.član())

			elif self >= {TEX.MSLOVO, TEX.VSLOVO, TEX.RAZLOMAK, TEX.VOTV}:
				if self >= {TEX.VOTV}:
					zagrada = True
				return Umnožak(zagrada, prvi, self.član())

			return prvi

	def član(self):
		if self >> {TEX.MSLOVO, TEX.VSLOVO}:
			return self.zadnji
		elif self >> TEX.VOTV:
			el = self.element()
			self.pročitaj(TEX.VZATV)
			return el

	start=izraz


class Izraz(AST('elementi')):
	def širina(self):
		suma=0
		for element in self.elementi:
			suma += element.širina()
		return suma
		#return [element.širina() for element in self.elementi]

class Zbroj(AST('zagrada prvi drugi')):
	def širina(self):
		if self.zagrada:
			return self.prvi.širina() + self.drugi.širina()	+ 14
		else:
			return self.prvi.širina() + self.drugi.širina() + 16

class Umnožak(AST('zagrada prvi drugi')): #ipak mi za umnozak ne idu zagrade!
	def širina(self):
		#if self.zagrada:
			#return self.prvi.širina() + self.drugi.širina()
		#else:
		return self.prvi.širina() + self.drugi.širina()

class Razlomak(AST('zagradeb zagraden brojnik nazivnik')):
	def širina(self):
		#ipak ne dodajem 2 ako je zagrada jer mi to umnožak (ne) radi
		if self.zagradeb:
			br = self.brojnik.širina()
		else: br = self.brojnik.širina()
		if self.zagraden:
			naz = self.nazivnik.širina()
		else:
			naz = self.nazivnik.širina()
		return max(br, naz) + 2 # dva za rubove razlomacke crte


if __name__ == '__main__':
	#\\frac{ab}CH+d
	ulaz1 = '\\frac{ab}CH+b'
	ulaz2 = '\\frac a b'


	print(ulaz1)
	#leksiranje
	tokeni = list(TEX_lex(ulaz1))#ispis tokena
	#otpakirana lista
	print(*tokeni)
	print(TEX_Parser.parsiraj(tokeni))
	print( TEX_Parser.parsiraj(tokeni).širina())
