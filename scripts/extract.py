import glob
import os
import shutil
import sqlite3
import pandas as pd

os.makedirs("data", exist_ok=True)

# 1. Prüfung auf Health Connect SQLite-Datenbank (.db)
db_files = glob.glob("raw_export/**/*.db", recursive=True)
if db_files:
    print(f"SQLite-Datenbank gefunden: {db_files}")
    conn = sqlite3.connect(db_files)
    # Alle verfügbaren Tabellen anzeigen (hilfreich fürs Debugging im Log)
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
    print("Enthaltene Tabellen:", tables["name"].tolist())
    
    if "nutrition_record_table" in tables["name"].values:
        df = pd.read_sql_query("SELECT * FROM nutrition_record_table", conn)
        df.to_csv("data/nutrition_latest.csv", index=False)
        print(f"Erfolgreich extrahiert: data/nutrition_latest.csv ({len(df)} Zeilen)")
    conn.close()

# 2. Prüfung auf direkte Samsung Health CSVs
for target in ["food_intake", "food_info", "nutrition"]:
    matches = glob.glob(f"raw_export/**/*{target}*.csv", recursive=True)
    if matches:
        latest_match = sorted(matches)[-1]
        df = pd.read_csv(latest_match, header=1, index_col=False)
        out_path = f"data/samsung_{target}.csv"
        df.to_csv(out_path, index=False)
        print(f"Erfolgreich extrahiert: {out_path} ({len(df)} Zeilen)")

shutil.rmtree("raw_export", ignore_errors=True)
