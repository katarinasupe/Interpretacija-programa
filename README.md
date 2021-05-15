# New Language (NL)

Zadatak nam je bio osmisliti programski jezik koji zadovoljava neke operacije i karakteristike koje inače očekujemo da jezik podržava. Tako naš NL jezik podržava 2 tipa podataka, broj (`BROJ`) i string (`STRING`), pri tome se strigovi zadaju unutar dvostrukih navodnika (" "), dok je broj samo niz znamenki bez razmaka. Nazivi varijabli (`IME`) su također strigovi, ali ne pisani unutar " ", nego u smislu da nazivi varijabli ne smiju početi brojem, već mora početi slovom. Također želimo da NL prepoznaje i obavlja i neke naredbe, pa kako bi NL neki izraz prepoznao kao naredbu on mora završiti sa ; (`TOČKAZAREZ`). 
 
**Primjer.** x = 1, y = "1"; 
x i y su varijable s time da je varijabli x pridružena vrijednost 1 tipa broj, a y vrijednsot1 tipa string.

U jeziku je još definirana i klasa `BREAK` koja služi za izlazak iz petlje.

## Pridruživanja

* **=** (`PRIDRUŽIVANJE`) - kako bismo svaku varijablu mogli inicijalizirati nekom vrijednošću ili joj kasnije pridružiti neku drugu vrijednost
* **+=**, **-=** (`PJEDNKO`,`MIJEDNAKO`) - kako bismo mogli povećavati/smanjiti vrijednost nekog ranije inicijaliziranog izraza za određenu vrijednost
* **++** , **- -** (`PPLUS`,`MMINUS`) - služi nam za (post/pred)inkrement/dekrement, tj. povećava/smanjuje vrijednost varijable za 1

## Operacije s tipovima

Kako bismo išta mogli raditi s varijablama i vrijednostima koje unesemo, trebaju nam neke specifične operacije za svaki od podržanih tipova podataka.

### Broj

#### Osnovne operacije:
* **+** (`PLUS`)
* **-** (`MINUS`)
* __*__ (`PUTA`)
* **/** (`KROZ`)

#### Usporedbe:
* **<** (`MANJE`), **<=** (`MJEDNAKO`)
* **>** (`VEĆE`), **=>** (`VJEDNAKO`)
* **==** (`JEDNAKO`), **!=** (`NJEDNAKO`)

#### Cast
* pretvaranje broja u string (`TOSTRING`)

```cpp
toInt(varijabla, broj);

ime = broj;
toInt(varijabla, ime);
```

Kako su podržani i negativni brojevi, treba naglasiti da ako je negativan broj prvi u izrazu onda nisu nužne zagrade, ali ako je ispred njega znak operacije, potrebne su zagrade.

**Primjer.** x = -2 * (-3);

### String

#### Osnovne operacije:
* **+** (`PLUS`) - kod stringa ova operacija predstavlja konkatenaciju

#### Usporedbe:
* **==** (`JEDNAKO`)

#### Cast
* pretvaranje stringa u broj (`TOINT`)

```cpp
toString(varijabla, broj);

ime = broj;
toString(varijabla, ime);
```

Osnovne operacije ne prihvaćaju _mješovite_ tipove, npr. `BROJ`+`STRING`, ali ako želimo takve izraze prvo operandi moraju pretvoriti u isti tip, a pri tome nam pomažu funkcije `TOSTRING` i  `TOINT`.
Operacije usporedbe vraćaju 1 (ako je izraz istinit) i 0 (ako je izraz lažan).


## Grananja

* **if** (`IF`)
```cpp
if(uvjet)
	kod
```
* **if-else** (`IF`, `ELSE`) 
```cpp
if(uvjet)
	kod
else
	kod
```

## Petlje
 
* **for** (`FOR`) 

```cpp
for(i=broj1;i<broj2;i++)
	kod
```
Pri tome gornja ograda može biti: 
* i<broj2
* i<=broj2
* i>broj2
* i>=broj2
 Pri tome je broj2 broj koji je veći ili jednak 0.

Dok vrijednost varijable _i_ možemo mijenjati sa ++ (`i++`,`++i`), --(`i--`,`--i`), +=, -=.


* **while** (`WHILE`)

```cpp
while(uvjet)
	kod
```

* **do-while** (`DO`,`WHILE`)

```cpp
do
	kod
while;
```
Primjetimo, _kod_ može biti jedna naredba ili više njih, a u slučaju da ih je više sve naredbe se nalaze u vitičastim zagradama, (`VOTV`,`VZATV`). Također, uvjet, se odnosi isključivo na **jedan** uvjet, ne na više njih.

## Unos, ispis

* **unos** (`CIN`) - omogućava korisniku unos brojeva i stringova s tipkovnice
* **ispis** (`COUT`) - NL ima mogućnost ispisa broja, stringa, te vrijednosti varijabli


## Komentari

NL prepoznaje 2 vrste komentara:
* **linijski** (`//`)
* **višelinijski** (`/**/`)

