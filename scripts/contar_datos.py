import pandas as pd
import os

base = "/root/mi_asistente_ia/data"
for f in ["investigadores.csv", "investigadores_funcionales.csv", "investigadores_original.csv", "investigadores_ejemplo.csv", "datos_prueba.csv"]:
    path = os.path.join(base, f)
    if not os.path.exists(path):
        print(f, "-> NO EXISTE")
        continue
    try:
        df = pd.read_csv(path, sep="|", engine="python")
        print(f, "->", len(df), "filas x", len(df.columns), "columnas (sep=|)")
    except Exception:
        try:
            df = pd.read_csv(path)
            print(f, "->", len(df), "filas x", len(df.columns), "columnas (sep=,)")
        except Exception as e2:
            print(f, "ERROR", e2)
