"""
Dieses Skript beschreibt verschiedene Pitfalls im Umgang mit mathematischen Berechnungen
in Python.
"""

# Imports
import time
import pandas as pd

"""
1.) Rechnen mit grossen Ganzzahlen in Python:
Python ist für die mathematische Forschung praedistintiert, da es
beliebig große Ganzzahlen verarbeiten kann. Hierzu muss man einige Pitfalls vermeiden.
"""

# Falsch: Anwendung einer Division mit nur einem Schraegstrich. Bei dieser Operation wird
# die Zahl in den Datentyp "float" konvertiert. Hierbei kommt es zu einem
# Genauigkeitsverlust. Nur der Datentyp "int" kann beliebig grosse Zahlen speichern
# und verarbeiten.
valid = 5**205 == (5**205 / 5) * 5
print("Division (Falsch):", valid)

# Richtig: Anwendung einer ganzzahligen Division mit zwei Schraegstrichen. Bei dieser Operation
# bleibt die Genauigkeit erhalten. Voraussetzung für die Korrektheit: Anwendbarkeit der ganzzahligen
# Division (nicht fuer Fliesskommazahlen geeignet).
valid = 5**205 == (5**205 // 5) * 5
print("Division (Richtig):", valid)

# Falsch: Berechnungen mit einem "float", anstatt mit einer Ganzzahl. Auch hier kommt es zu
# einer Typkonversion mit Genauigkeitsverlust.
valid = 5**205 + 1 == 5**205 + 1.0
print("Weitere Berechnungen (Falsch):", valid)

# Richtig: Berechnungen mit Ganzzahlen ohne Komma.
valid = 5**205 + 1 == 5 ** 205 + 1
print("Weitere Berechnungen (Richtig):", valid)

"""
2.) Umgang mit grossen Ganzzahlen in Pandas:
Auch in Pandas kann man mit beliebig großen Ganzzahlen arbeiten. Hier die Pitfalls:
"""

# Falsch: Berechnen grosser Zahlen direkt in einer Series oder einem DataFrame.
# Der intern verwendete Pandas Datentyp "int64" ist in seiner Genauigkeit begrenzt.
my_numbers = pd.Series([5, 6])
my_exponents = pd.Series([205, 206])
my_powers = my_numbers ** my_exponents
valid = list(my_powers) == [5**205, 6**206]
print("Berechnung in Pandas (Falsch):", valid)
print("Datatype:", my_powers.dtype)

# Richtig (Alternative 1): Berechnen der großen Zahlen ausserhalb der Series oder
# des DataFrames. Werden die Zahlen extern berechnet, werden sie bei der Erzeugung der
# der Series / des DataFrames im Datentyp "object" gespeichert. Die Genauigkeit
# bleibt erhalten.
my_powers = pd.Series([5**205, 6**206])
valid = list(my_powers) == [5**205, 6**206]
print("Berechnung in Pandas (Alternative 1):", valid)
print("Datatype:", my_powers.dtype)

# Richtig (Alternative 2): Berechnung der Zahlen mit Hilfe einer Lambda-Funktion
# im DataFrame.
my_numbers = pd.Series([5, 6])
my_exponents = pd.Series([205, 206])
my_frame = pd.DataFrame({
    "number": my_numbers, "exponent": my_exponents})

my_frame["power"] = my_frame.apply(
    lambda x: int(x["number"]) ** int(x["exponent"]), axis=1)

valid = list(my_frame["power"]) == [5**205, 6**206]
print("Berechnung in Pandas (Alternative 2):", valid)
print("Datatype:", my_frame["power"].dtype)


"""
3.) Pandas DataFrames koennen mit relativ vielen Zahlen umgehen. Um eine effiziente
Verarbeitung zu gewahrleisten, muss folgendes beachtet werden.
"""

# Langsam: Iteratives Einfuegen einzelner Zahlen.
print("Einfuegen (Falsch) Start:", time.asctime())
my_numbers = pd.DataFrame({
    "number": []
})

for i in range(10000):
    my_numbers = my_numbers.append(pd.DataFrame({"number": [i]}), ignore_index=True)

my_numbers.reset_index(drop=True)
print("Einfuegen (Falsch) Ende:", time.asctime())
print(my_numbers.head())

# Schnell: Iteratives Einfuegen der Zahlen zunächst in eine Python-Liste. Dann gesammelte
# Erzeugung eines DataFrames.
print("Einfuegen (Richtig) Start:", time.asctime())
my_list = []

for i in range(10000):
    my_list.append(i)

my_numbers = pd.DataFrame({
    "number": my_list
})

print("Einfuegen (Richtig) Ende:", time.asctime())
print(my_numbers.head())
