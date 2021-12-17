# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 20:18:13 2021

@author: Jakub
"""
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.animation as ani
import numpy as np

# Odczytuje plik z sieci 
df = pd.read_excel("https://github.com/jakubrybacki/Karowa_Python_Introduction/raw/main/Zajecia%2010/chart3.xlsx")

# Wyznaczam kolumne z datami jako indeks dla wszystkich kolumn DataFrame
df = df.set_index('Date')

# Wybieram interesujące mnie kolumny
df2 = df[['CZ', 'DE', 'ES', 'FR', 'IT', 'HU', 'NL', 'PL', 'SK', 'FI', 'SE']]

# Tworze słownik opisujacy kolor jaki ma reprezentowac panstwo na wykresie
colors_dict = {'CZ': "#FFC000", # Zolty
          'DE': "#000000", # Czarny
          'ES': "#60060A", # Czerwony
          'FR': "#002395", # Niebieski
          'IT': "#00B050", # Zielony
          'HU': "#7f00ff", # Fiolet
          'NL': "#FFA500", # Pomarancz  
          'PL': "#D22630", # Czerwien
          'SK': "#2CD4E2", # Seledynowy
          'FI': "#002F6C", # Niebieski   
          'SE': "#FECC02" # Zolty
}

# Zaczynam tworzyć wykres
fig, ax = plt.subplots()
bar = ''

# Funkcja opisujaca generowanie animacji:
def animeFunciton(i=int):
    # Czyszcze dotychczasowa zawartosc wykresu
    ax.clear()
    
    # Ustawiam 
    ax.set_ylim([0, 50])
    
    # Sortuje indeksy z nazwami krajow po warsciach  
    objects = df2.iloc[i].sort_values(ascending=False).index
    
    # Sztuczka: Bibliotek Numpy pomaga ustalic szerokosc na wykresie
    y_pos = np.arange(len(objects))
    
    
    # Przypisuje posortowane wartosci do drugiej listy
    performance = df2.iloc[i].sort_values(ascending=False).values.tolist()
    
    # Tworze kolumny - zwrorcie uwage na zmienna Color. Kazdorazowo bedzie zalezna od slownika
    plt.bar(y_pos, performance, align='center', color=[colors_dict[x] for x in objects])
    
    # Pomniejsze formatowania: 
    plt.xticks(y_pos, objects)
    plt.ylabel('Odsetek firm z niedoborem pracowników')
    plt.xlabel('Kraje')
    plt.title('Niedobory pracowników w ' + df.index[i],
              loc='center', fontweight="bold", fontname="Arial Black")

# Tworze klatki dla animacji
# Sztuczka: Opdowiednio manipulujac petla wrzucam więcej klatek z animacja ostatnich 8 okresów
frames_arg = []
for i in range(48):
    for j in range(5):
        frames_arg.append(i)
    if i >= 40:
        for j in range(5):
            frames_arg.append(i)        

# Funkcja animujaca
animator = ani.FuncAnimation(fig, animeFunciton, frames = frames_arg, interval=1_000)

# Zapis do pliku
writergif = ani.ImageMagickFileWriter()
animator.save("shortage.gif", writer = writergif)
