import csv
import sys

path = sys.argv[1]
raw = open(path, "rb").read()
print("BOM:", raw[:3] == b"\xef\xbb\xbf")
print("CRLF presente:", b"\r\n" in raw)
print("tamano bytes:", len(raw))

with open(path, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter="|")
    print("num columnas:", len(reader.fieldnames))
    for i, row in enumerate(reader, 1):
        vals = list(row.values())
        n_none = sum(1 for v in vals if v is None)
        autor = (row.get("identificacion") or "")[:35]
        print(f"fila {i}: campos={len(vals)} nulos={n_none} ident='{autor}...'")
