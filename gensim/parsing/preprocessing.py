#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import re
import string
import glob

from gensim import utils
from nltk.stem.snowball import GermanStemmer
#from gensim.parsing.porter import PorterStemmer


# improved list from Stone, Denis, Kwantes (2010)
STOPWORDS = """
ab
bei
da
deshalb
ein
für
haben
hier
ich
ja
kann
machen
muesste
nach
oder
seid
sonst
und
vom
wann
wenn
wie
zu
bin
eines
hat
manche
solches
an
anderm
bis
das
deinem
demselben
dir
doch
einig
er
eurer
hatte
ihnen
ihre
ins
jenen
keinen
manchem
meinen
nichts
seine
soll
unserm
welche
werden
wollte
während
alle
allem
allen
aller
alles
als
also
am
ander
andere
anderem
anderen
anderer
anderes
andern
anders
auch
auf
aus
bist
bsp.
daher
damit
dann
dasselbe
dazu
daß
dein
deine
deinen
deiner
deines
dem
den
denn
denselben
der
derer
derselbe
derselben
des
desselben
dessen
dich
die
dies
diese
dieselbe
dieselben
diesem
diesen
dieser
dieses
dort
du
durch
eine
einem
einen
einer
einige
einigem
einigen
einiger
einiges
einmal
es
etwas
euch
euer
eure
eurem
euren
eures
ganz
ganze
ganzen
ganzer
ganzes
gegen
gemacht
gesagt
gesehen
gewesen
gewollt
hab
habe
hatten
hin
hinter
ihm
ihn
ihr
ihrem
ihren
ihrer
ihres
im
in
indem
ist
jede
jedem
jeden
jeder
jedes
jene
jenem
jener
jenes
jetzt
kein
keine
keinem
keiner
keines
konnte
können
könnte
mache
machst
macht
machte
machten
man
manchen
mancher
manches
mein
meine
meinem
meiner
meines
mich
mir
mit
muss
musste
müßt
nicht
noch
nun
nur
ob
ohne
sage
sagen
sagt
sagte
sagten
sagtest
sehe
sehen
sehr
seht
sein
seinem
seinen
seiner
seines
selbst
sich
sicher
sie
sind
so
solche
solchem
solchen
solcher
sollte
sondern
um
uns
unse
unsen
unser
unses
unter
viel
von
vor
war
waren
warst
was
weg
weil
weiter
welchem
welchen
welcher
welches
werde
wieder
will
wir
wird
wirst
wo
wolle
wollen
wollt
wollten
wolltest
wolltet
würde
würden
z.B.
zum
zur
zwar
zwischen
über
aber
abgerufen
abgerufene
abgerufener
abgerufenes
acht
allein
allerdings
allerlei
allgemein
allmählich
allzu
alsbald
andererseits
andernfalls
anerkannt
anerkannte
anerkannter
anerkanntes
anfangen
anfing
angefangen
angesetze
angesetzt
angesetzten
angesetzter
ansetzen
anstatt
arbeiten
aufgehört
aufgrund
aufhören
aufhörte
aufzusuchen
ausdrücken
ausdrückt
ausdrückte
ausgenommen
ausser
ausserdem
author
autor
außen
außer
außerdem
außerhalb
bald
bearbeite
bearbeiten
bearbeitete
bearbeiteten
bedarf
bedurfte
bedürfen
befragen
befragte
befragten
befragter
begann
beginnen
begonnen
behalten
behielt
beide
beiden
beiderlei
beides
beim
beinahe
beitragen
beitrugen
bekannt
bekannte
bekannter
bekennen
benutzt
bereits
berichten
berichtet
berichtete
berichteten
besonders
besser
bestehen
besteht
beträchtlich
bevor
bezüglich
bietet
bisher
bislang
bis
bleiben
blieb
bloss
bloß
brachte
brachten
brauchen
braucht
bringen
bräuchte
bzw
böden
ca.
dabei
dadurch
dafür
dagegen
dahin
damals
danach
daneben
dank
danke
danken
dannen
daran
darauf
daraus
darf
darfst
darin
darum
darunter
darüber
darüberhinaus
dass
davon
davor
demnach
denen
dennoch
derart
derartig
derem
deren
derjenige
derjenigen
derzeit
desto
deswegen
diejenige
diesseits
dinge
direkt
direkte
direkten
direkter
doppelt
dorther
dorthin
drauf
drei
dreißig
drin
dritte
drunter
drüber
dunklen
durchaus
durfte
durften
dürfen
dürfte
eben
ebenfalls
ebenso
ehe
eher
eigenen
eigenes
eigentlich
einbaün
einerseits
einfach
einführen
einführte
einführten
eingesetzt
einigermaßen
eins
einseitig
einseitige
einseitigen
einseitiger
einst
einstmals
einzig
ende
entsprechend
entweder
ergänze
ergänzen
ergänzte
ergänzten
erhalten
erhielt
erhielten
erhält
erneut
erst
erste
ersten
erster
eröffne
eröffnen
eröffnet
eröffnete
eröffnetes
etc
etliche
etwa
fall
falls
fand
fast
ferner
finden
findest
findet
folgende
folgenden
folgender
folgendes
folglich
fordern
fordert
forderte
forderten
fortsetzen
fortsetzt
fortsetzte
fortsetzten
fragte
frau
frei
freie
freier
freies
fuer
fünf
gab
ganzem
gar
gbr
geb
geben
geblieben
gebracht
gedurft
geehrt
geehrte
geehrten
geehrter
gefallen
gefiel
gefälligst
gefällt
gegeben
gehabt
gehen
geht
gekommen
gekonnt
gemocht
gemäss
genommen
genug
gern
gestern
gestrige
getan
geteilt
geteilte
getragen
gewissermaßen
geworden
ggf
gib
gibt
gleich
gleichwohl
gleichzeitig
glücklicherweise
gmbh
gratulieren
gratuliert
gratulierte
gute
guten
gängig
gängige
gängigen
gängiger
gängiges
gänzlich
haette
halb
hallo
hast
hattest
hattet
heraus
herein
heute
heutige
hiermit
hiesige
hinein
hinten
hinterher
hoch
hundert
hätt
hätte
hätten
höchstens
igitt
immer
immerhin
important
indessen
info
infolge
innen
innerhalb
insofern
inzwischen
irgend
irgendeine
irgendwas
irgendwen
irgendwer
irgendwie
irgendwo
je
jedenfalls
jederlei
jedoch
jemand
jenseits
jährig
jährige
jährigen
jähriges
kam
kannst
kaum
keines
keinerlei
keineswegs
klar
klare
klaren
klares
klein
kleinen
kleiner
kleines
koennen
koennt
koennte
koennten
komme
kommen
kommt
konkret
konkrete
konkreten
konkreter
konkretes
konnten
könn
könnt
könnten
künftig
lag
lagen
langsam
lassen
laut
lediglich
leer
legen
legte
legten
leicht
leider
lesen
letze
letzten
letztendlich
letztens
letztes
letztlich
lichten
liegt
liest
links
längst
längstens
mag
magst
mal
mancherorts
manchmal
mann
margin
mehr
mehrere
meist
meiste
meisten
meta
mindestens
mithin
mochte
morgen
morgige
muessen
muesst
musst
mussten
muß
mußt
möchte
möchten
möchtest
mögen
möglich
mögliche
möglichen
möglicher
möglicherweise
müssen
müsste
müssten
müßte
nachdem
nacher
nachhinein
nahm
natürlich
nacht
neben
nebenan
nehmen
nein
neu
neue
neuem
neuen
neuer
neues
neun
nie
niemals
niemand
nimm
nimmer
nimmt
nirgends
nirgendwo
nutzen
nutzt
nutzung
nächste
nämlich
nötigenfalls
nützt
oben
oberhalb
obgleich
obschon
obwohl
oft
per
pfui
plötzlich
pro
reagiere
reagieren
reagiert
reagierte
rechts
regelmäßig
rief
rund
sang
sangen
schlechter
schließlich
schnell
schon
schreibe
schreiben
schreibens
schreiber
schwierig
schätzen
schätzt
schätzte
schätzten
sechs
sect
sehrwohl
sei
seit
seitdem
seite
seiten
seither
selber
senke
senken
senkt
senkte
senkten
setzen
setzt
setzte
setzten
sicherlich
sieben
siebte
siehe
sieht
singen
singt
sobald
sodaß
soeben
sofern
sofort
sog
sogar
solange
solc hen
solch
sollen
sollst
sollt
sollten
solltest
somit
sonstwo
sooft
soviel
soweit
sowie
sowohl
spielen
später
startet
startete
starteten
statt
stattdessen
steht
steige
steigen
steigt
stets
stieg
stiegen
such
suchen
sämtliche
tages
tat
tatsächlich
tatsächlichen
tatsächlicher
tatsächliches
tausend
teile
teilen
teilte
teilten
titel
total
trage
tragen
trotzdem
trug
trägt
tun
tust
tut
txt
tät
ueber
umso
unbedingt
ungefähr
unmöglich
unmögliche
unmöglichen
unmöglicher
unnötig
unsem
unser
unsere
unserem
unseren
unserer
unseres
unten
unterbrach
unterbrechen
unterhalb
unwichtig
usw
vergangen
vergangene
vergangener
vergangenes
vermag
vermutlich
vermögen
verrate
verraten
verriet
verrieten
version
versorge
versorgen
versorgt
versorgte
versorgten
versorgtes
veröffentlichen
veröffentlicher
veröffentlicht
veröffentlichte
veröffentlichten
veröffentlichtes
viele
vielen
vieler
vieles
vielleicht
vielmals
vier
vollständig
voran
vorbei
vorgestern
vorher
vorne
vorüber
völlig
während
wachen
waere
warum
weder
wegen
weitere
weiterem
weiteren
weiterer
weiteres
weiterhin
weiß
wem
wen
wenig
wenige
weniger
wenigstens
wenngleich
wer
werdet
weshalb
wessen
wichtig
wieso
wieviel
wiewohl
willst
wirklich
wodurch
wogegen
woher
wohin
wohingegen
wohl
wohlweislich
womit
woraufhin
woraus
worin
wurde
wurden
währenddessen
wär
wäre
wären
zahlreich
zehn
zeitweise
ziehen
zieht
zog
zogen
zudem
zuerst
zufolge
zugleich
zuletzt
zumal
zurück
zusammen
zuviel
zwanzig
zwei
zwölf
ähnlich
übel
überall
überallhin
überdies
übermorgen
übrig
übrigens
"""
STOPWORDS = frozenset(w for w in STOPWORDS.split() if w)


def remove_stopwords(s):
    s = utils.to_unicode(s)
    return " ".join(w for w in s.split() if w not in STOPWORDS)


RE_PUNCT = re.compile('([%s])+' % re.escape(string.punctuation), re.UNICODE)
def strip_punctuation(s):
    s = utils.to_unicode(s)
    return RE_PUNCT.sub(" ", s)


# unicode.translate cannot delete characters like str can
strip_punctuation2 = strip_punctuation
# def strip_punctuation2(s):
#     s = utils.to_unicode(s)
#     return s.translate(None, string.punctuation)


RE_TAGS = re.compile(r"<([^>]+)>", re.UNICODE)
def strip_tags(s):
    s = utils.to_unicode(s)
    return RE_TAGS.sub("",s)


def strip_short(s, minsize=3):
    s = utils.to_unicode(s)
    return " ".join(e for e in s.split() if len(e) >= minsize)


RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)
def strip_numeric(s):
    s = utils.to_unicode(s)
    return RE_NUMERIC.sub("", s)


RE_NONALPHA = re.compile(r"\W", re.UNICODE)
def strip_non_alphanum(s):
    s = utils.to_unicode(s)
    return RE_NONALPHA.sub(" ", s)


RE_WHITESPACE = re.compile(r"(\s)+", re.UNICODE)
def strip_multiple_whitespaces(s):
    s = utils.to_unicode(s)
    return RE_WHITESPACE.sub(" ", s)


RE_AL_NUM = re.compile(r"([a-z]+)([0-9]+)", flags=re.UNICODE)
RE_NUM_AL = re.compile(r"([0-9]+)([a-z]+)", flags=re.UNICODE)
def split_alphanum(s):
    s = utils.to_unicode(s)
    s = RE_AL_NUM.sub(r"\1 \2", s)
    return RE_NUM_AL.sub(r"\1 \2", s)


def stem_text(text):
    text = utils.to_unicode(text)
    p = GermanStemmer()
    return ' '.join(p.stem(word) for word in text.split())
stem = stem_text

DEFAULT_FILTERS = [lambda x: x.lower(), strip_tags, strip_punctuation, strip_multiple_whitespaces,
                   strip_numeric, remove_stopwords, strip_short, stem_text]


def preprocess_string(s, filters=DEFAULT_FILTERS):
    s = utils.to_unicode(s)
    for f in filters:
        s = f(s)
    return s.split()


def preprocess_documents(docs):
    return [preprocess_string(d) for d in docs]


def read_file(path):
    with utils.smart_open(path) as fin:
        return fin.read()


def read_files(pattern):
    return [read_file(fname) for fname in glob.glob(pattern)]
