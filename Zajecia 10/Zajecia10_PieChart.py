# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 11:03:02 2021

@author: Jakub
"""
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.animation as ani
import os

# Animacja którą wykorzystąłem do promowania komentarza do inflacji:
# https://twitter.com/jakubrybacki2/status/1471048562519818242?s=20

# Komenda ustawia ścieżkę do zapisu na ta, gdzie wykonywany jest skrytp
filePath = os.getcwd() + "\\"

#Dane z Excela z projekcją:
# https://www.nbp.pl/home.aspx?f=/polityka_pieniezna/dokumenty/projekcja_inflacji.html
dict_projekcja = { "Rok": [2021,2022, 2023],
                   "Inflacja bazowa": [4.0, 4.1, 3.5],
                   "Ceny żywności":[2.8, 4.1, 2.9],
                   "Ceny energii": [11.8, 14.8, 5.1]
                 }

# Wagi z koszyka CPI
waga_core = 0.6
waga_food = 0.27
waga_energia = 1 - waga_core - waga_food

# Wyliczam kontrybucje
dane_kontrybucje = pd.DataFrame(dict_projekcja)
dane_kontrybucje["Inflacja bazowa"] = dane_kontrybucje["Inflacja bazowa"] * waga_core
dane_kontrybucje["Ceny żywności"] = dane_kontrybucje["Ceny żywności"] * waga_food
dane_kontrybucje["Ceny energii"] = dane_kontrybucje["Ceny energii"] * waga_energia

# Wyliczam procentowe udzialy poszczegolnych grup cen w inflacji 
dane_procentowe = dane_kontrybucje.copy()
dane_procentowe["Inflacja bazowa"] = dane_kontrybucje["Inflacja bazowa"]/(dane_kontrybucje["Inflacja bazowa"] + dane_kontrybucje["Ceny żywności"] + dane_kontrybucje["Ceny energii"])
dane_procentowe["Ceny żywności"] = dane_kontrybucje["Ceny żywności"]/(dane_kontrybucje["Inflacja bazowa"] + dane_kontrybucje["Ceny żywności"] + dane_kontrybucje["Ceny energii"])
dane_procentowe["Ceny energii"] = dane_kontrybucje["Ceny energii"]/(dane_kontrybucje["Inflacja bazowa"] + dane_kontrybucje["Ceny żywności"] + dane_kontrybucje["Ceny energii"])

#Parametr okrela które elementy wyswietlac i w jakiej kolejnosci
framesArg = [#0,0,0,0,0,0,0,0,0,0, 
             1,1,1,1,1,1,1,1,1,1,
             2,2,2,2,2,2,2,2,2,2]

# Wykres
fig,ax = plt.subplots()

# Dla skrocenia kodu zapisuje interesujace mnie serie danych do nowego obiektu
temp = dane_procentowe[["Inflacja bazowa", "Ceny żywności", "Ceny energii"]]

def animeFunction(i):
    # Komenda poniżej każdorazowo czyści wykres
    ax.clear()
    
    # W tym miejscu rysuje wykres kolowy - iloc okresla numer wiersza w DataFrame do którego się odwoluje
    plot = temp.iloc[i].plot(kind='pie', ax=ax, autopct='%1.1f%%', colors = ['#D22630', '#7F7F7F','#FFC000'])
    
    # Ta komenda aktualizuje tytul
    plot.set_title('Struktura inflacji wg. projekcji NBP - rok ' + str(dane_procentowe.Rok[i]), 
                   loc='center', fontweight="bold", fontname="Arial Black")
    
    # Wykresy kolowe maja domyslnie niepotrzebna etykiete - w ten sposob ja czyszcze
    ax.set_ylabel("")

animator = ani.FuncAnimation(fig, func = animeFunction, frames=framesArg, interval = 10_000)

# Zapis do pliku
writergif = ani.ImageMagickFileWriter()
animator.save(filePath + "NBP.gif", writer = writergif)
