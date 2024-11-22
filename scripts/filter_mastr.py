import sqlite3
import pandas as pd
import os

# Datenbankpfad
db_path = r'C:\Users\LenovoTPX13\.open-MaStR\data\sqlite\open-mastr.db'

# Verzeichnis, in dem die CSV-Dateien gespeichert werden sollen
output_dir = '../data/filtered_data_mastr_20240916'

# Unterordner für die einzelnen Postleitzahlgebiete
plz_folders = {
    '10589': os.path.join(output_dir, '10589'), # Berlin Mierendorfinsel
    
}

# Überprüfen, ob die Verzeichnisse existieren, ansonsten erstellen
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for folder in plz_folders.values():
    if not os.path.exists(folder):
        os.makedirs(folder)

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(db_path)

# Funktion zum Abrufen der Tabellennamen
def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

# Funktion zum Abrufen der Spaltennamen einer Tabelle
def get_column_names(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return [column[1] for column in columns]

# Funktion zur Bereinigung von problematischen Zeichen und zur Umwandlung von Dezimaltrennzeichen in DataFrames
def clean_and_convert_data(df):
    # Definiere problematische Zeichen und ersetze sie durch '?'
    problematische_zeichen = {
        '\uff06': '&',  # Problematisches "&"-Zeichen ersetzen
        '\u2013': '-',  # En-Dash ersetzen durch Minuszeichen
    }
    
    # Bereinige problematische Zeichen, aber überspringe die Spalte "Postleitzahl"
    df_cleaned = df.applymap(lambda x: ''.join(problematische_zeichen.get(c, c) for c in x) if isinstance(x, str) else x)

    # Numerische Spalten finden und Komma durch Punkt ersetzen (überspringe "Postleitzahl")
    for col in df_cleaned.select_dtypes(include='object').columns:
        if col != 'Postleitzahl':  # "Postleitzahl" soll nicht umgewandelt werden
            try:
                # Ersetze Komma durch Punkt und konvertiere in float
                df_cleaned[col] = df_cleaned[col].str.replace(',', '.').astype(float)
            except ValueError:
                # Wenn keine Umwandlung möglich ist, ignoriere die Spalte
                pass

    return df_cleaned

# Tabellennamen abrufen
tables = get_table_names(conn)

# Liste der Postleitzahlen, nach denen wir filtern wollen
plz_values = ['10589; 10553 '] # Waldau Kassel: 34123, Fuldatal: 34277, Lohfelden: 34253, '34123', '34277', '34253'

# Dictionary, um die DataFrames zu speichern
dataframes = {}

# Durch alle Tabellen iterieren
for table in tables:
    # Spaltennamen der Tabelle abrufen
    columns = get_column_names(conn, table)

    # Prüfen, ob die Tabelle eine Spalte "Postleitzahl" enthält
    if 'Postleitzahl' in columns:
        # SQL-Abfrage definieren, um die gewünschten Datensätze zu filtern
        query = f"""
        SELECT * 
        FROM {table}
        WHERE Postleitzahl IN ({','.join(['?' for _ in plz_values])})
        """
        
        # Daten aus der Tabelle abfragen und in ein Pandas DataFrame laden
        df = pd.read_sql_query(query, conn, params=plz_values)
        
        # Nur DataFrames speichern, die auch Daten enthalten
        if not df.empty:
            # Bereinige problematische Zeichen und konvertiere Dezimaltrennzeichen in den Daten
            df_cleaned = clean_and_convert_data(df)
            # Das bereinigte DataFrame im Dictionary unter dem Tabellennamen speichern
            dataframes[table] = df_cleaned
            print(f"Datensätze aus der Tabelle {table} erfolgreich geladen und bereinigt.")
        else:
            print(f"Keine Datensätze in der Tabelle {table} mit den gewünschten Postleitzahlen gefunden.")
    else:
        print(f"Die Tabelle {table} enthält keine Spalte 'Postleitzahl'.")

# Verbindung schließen
conn.close()

# Hauptordner: Ausgabe der geladenen und bereinigten DataFrames und Speicherung in CSV-Dateien
for table, df in dataframes.items():
    csv_path = os.path.join(output_dir, f'{table}_filtered.csv')
    df.to_csv(csv_path, index=False, sep=';', encoding='latin1')  # Standard-Encoding 'latin1'
    print(f'Daten aus der Tabelle {table} wurden in {csv_path} gespeichert.')

# Für jedes Postleitzahlgebiet separate CSV-Dateien in den Unterordnern speichern
for table, df in dataframes.items():
    for plz, folder in plz_folders.items():
        # Filter für die aktuelle Postleitzahl
        df_plz = df[df['Postleitzahl'] == plz]
        
        # Nur speichern, wenn es Datensätze gibt
        if not df_plz.empty:
            csv_path = os.path.join(folder, f'{table}_PLZ_{plz}.csv')
            df_plz.to_csv(csv_path, index=False, sep=';', encoding='latin1')  # Standard-Encoding 'latin1'
            print(f'Daten für PLZ {plz} aus der Tabelle {table} wurden in {csv_path} gespeichert.')


