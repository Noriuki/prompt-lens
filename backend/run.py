#!/usr/bin/env python3
"""Run the Prompt Lens API server. From backend/: python run.py (com venv ativo e pip install -e .)."""

import sys
from pathlib import Path

# Ensure project root is on path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import uvicorn
except ModuleNotFoundError:
    print("Dependências não instaladas. Na pasta backend/:")
    print("  python3 -m venv .venv && source .venv/bin/activate")
    print("  pip install -e .")
    print("  python run.py")
    sys.exit(1)

if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
