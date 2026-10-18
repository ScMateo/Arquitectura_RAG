"""CLI: run the RAG evaluation harness (PLAN_VALIDACION.md).

Usage:
    cd Arquitectura_RAG
    PYTHONPATH=backend python scripts/evaluate.py
    PYTHONPATH=backend python scripts/evaluate.py --judge
    PYTHONPATH=backend python scripts/evaluate.py --collection cvlac_eval --limit 8
"""

import sys

from evaluation.runner import main

if __name__ == "__main__":
    sys.exit(main())
