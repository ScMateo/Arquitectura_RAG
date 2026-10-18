"""CLI: index a CvLAC CSV (data contract) into the vector store.

Usage:
    cd Arquitectura_RAG
    PYTHONPATH=backend python scripts/index.py data/sample/investigadores.csv
"""

import argparse
import sys
import time

from qdrant_client import QdrantClient

from app.api.dependencies import get_indexer
from app.core.config import get_settings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Indexa un CSV CvLAC conforme al contrato de datos (REGLAS_DATOS_CSV.md)."
    )
    parser.add_argument("csv_path", help="Ruta del archivo CSV a indexar.")
    args = parser.parse_args()

    settings = get_settings()
    indexer = get_indexer()

    print(f"Indexando: {args.csv_path}")
    start = time.perf_counter()
    indexer.index(args.csv_path)
    elapsed = time.perf_counter() - start

    client = QdrantClient(url=settings.qdrant_url)
    info = client.get_collection(settings.qdrant_collection)

    print(f"OK   coleccion : {settings.qdrant_collection}")
    print(f"OK   puntos    : {info.points_count}")
    print(f"OK   tiempo    : {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
