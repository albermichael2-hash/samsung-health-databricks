import glob
import os
import shutil
import pandas as pd

os.makedirs("data", exist_ok=True)
targets = ["food_intake", "food_info", "nutrition"]

for target in targets:
    matches = glob.glob(f"raw_export/**/*{target}*.csv", recursive=True)
    if matches:
        # Falls mehrere Dateien passen, nimm die neueste/größte
        latest_match = sorted(matches)[-1]
        df = pd.read_csv(latest_match, header=1, index_col=False)
        out_path = f"data/samsung_{target}.csv"
        df.to_csv(out_path, index=False)
        print(f"Erfolgreich extrahiert: {out_path} ({len(df)} Zeilen)")
    else:
        print(f"Warnung: Keine Datei für {target} im ZIP gefunden.")

# Temporären Ordner wieder aufräumen
shutil.rmtree("raw_export", ignore_errors=True)
