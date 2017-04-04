import pandas as pd

columns = ['Internationale Vorwahl', 'Telefon', 'Telefax', 'Straße-Adresse', 'Hausnummer', 'PLZ', 'Ort', 'Regierungsbezirk', 'Bundesland', 'Land', 'Zusätzl. Informationen', 'Rechtsform (kurz)', 'Hauptbranche WZ 2008']
data = ['+43', '07562 53100', '07562 53104', 'Windischgarsten', '15', '4580', 'Windischgarsten', 'Kirchdorf an der Krems', 'Oberösterreich', 'AT', 'Windischgarsten', 'eK', '\n10130\nFleischverarbeitung\n']

frame1 = pd.DataFrame(columns=columns)
row = pd.Series(data)
frame1 = frame1.append(row, ignore_index=True)
print(frame1.describe())
