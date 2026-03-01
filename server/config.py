from pathlib import Path

DIFFICULTY = 4
TARGET_PREFIX = "0" * DIFFICULTY
DATA_DIR = Path("data")
CHAIN_FILE = DATA_DIR / "chain.json"
LEDGER_FILE = DATA_DIR / "ledger.json"
HOST = "0.0.0.0"
PORT = 8000
