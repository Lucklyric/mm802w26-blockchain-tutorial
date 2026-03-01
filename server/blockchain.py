import json
import threading

from fastapi import HTTPException

from config import CHAIN_FILE, DATA_DIR, DIFFICULTY, LEDGER_FILE
from crypto_utils import compute_block_hash, verify_signature


class Blockchain:
    def __init__(self):
        self.chain: list[dict] = []
        self.ledger: dict[str, dict] = {}
        self.lock = threading.Lock()
        DATA_DIR.mkdir(exist_ok=True)
        self.load_chain()

    def _create_genesis_block(self) -> dict:
        data = {"miner_pubkey": "genesis", "miner_email": "system", "action": "genesis"}
        genesis = {
            "index": 0,
            "timestamp": 0.0,
            "data": data,
            "previous_hash": "0" * 64,
            "nonce": 0,
            "hash": compute_block_hash(0, 0.0, data, "0" * 64, 0),
            "signature": "genesis",
        }
        return genesis

    def load_chain(self):
        if CHAIN_FILE.exists():
            with open(CHAIN_FILE) as f:
                self.chain = json.load(f)
        else:
            self.chain = [self._create_genesis_block()]
            self.save_chain()
        if LEDGER_FILE.exists():
            with open(LEDGER_FILE) as f:
                self.ledger = json.load(f)
        else:
            self.ledger = {}
        for block in self.chain:
            self._update_ledger_from_block(block)

    def save_chain(self):
        with open(CHAIN_FILE, "w") as f:
            json.dump(self.chain, f, indent=2)

    def save_ledger(self):
        with open(LEDGER_FILE, "w") as f:
            json.dump(self.ledger, f, indent=2)

    def _update_ledger_from_block(self, block: dict):
        data = block["data"]
        email = data.get("miner_email")
        pubkey = data.get("miner_pubkey")
        if email and pubkey and email != "system":
            if email in self.ledger:
                self.ledger[email]["status"] = 1
                self.ledger[email]["block_index"] = block["index"]

    def register(self, pubkey: str, email: str) -> dict:
        for entry in self.ledger.values():
            if entry["pubkey"] == pubkey:
                raise HTTPException(status_code=400, detail="Public key already registered")
        if email in self.ledger:
            raise HTTPException(status_code=400, detail="Email already registered")
        self.ledger[email] = {"pubkey": pubkey, "status": 0}
        self.save_ledger()
        return {"success": True, "message": f"Registered {email}"}

    def submit_block(self, block_dict: dict) -> dict:
        with self.lock:
            if block_dict["index"] != len(self.chain):
                raise HTTPException(status_code=400, detail=f"Invalid index. Expected {len(self.chain)}")

            if block_dict["previous_hash"] != self.chain[-1]["hash"]:
                raise HTTPException(status_code=400, detail="Invalid previous_hash")

            data_dict = block_dict["data"]
            if isinstance(data_dict, dict):
                pass
            else:
                data_dict = data_dict.dict() if hasattr(data_dict, "dict") else dict(data_dict)

            recomputed = compute_block_hash(
                block_dict["index"],
                block_dict["timestamp"],
                data_dict,
                block_dict["previous_hash"],
                block_dict["nonce"],
            )
            if recomputed != block_dict["hash"]:
                raise HTTPException(status_code=400, detail="Hash mismatch")

            target = "0" * DIFFICULTY
            if not block_dict["hash"].startswith(target):
                raise HTTPException(status_code=400, detail=f"Hash does not meet difficulty (need {DIFFICULTY} leading zeros)")

            pubkey = data_dict["miner_pubkey"]
            email = data_dict["miner_email"]

            registered = False
            for e, entry in self.ledger.items():
                if entry["pubkey"] == pubkey:
                    registered = True
                    break
            if not registered:
                raise HTTPException(status_code=400, detail="Miner not registered")

            if email not in self.ledger or self.ledger[email]["pubkey"] != pubkey:
                raise HTTPException(status_code=400, detail="Email/pubkey mismatch")

            if self.ledger[email]["status"] == 1:
                raise HTTPException(status_code=400, detail="Miner already completed")

            if data_dict["action"] != "set_done":
                raise HTTPException(status_code=400, detail="Invalid action. Must be 'set_done'")

            if not verify_signature(pubkey, block_dict["signature"], block_dict["hash"]):
                raise HTTPException(status_code=400, detail="Invalid signature")

            self.chain.append(block_dict)
            self.ledger[email]["status"] = 1
            self.ledger[email]["block_index"] = block_dict["index"]
            self.save_chain()
            self.save_ledger()

            return {"success": True, "message": f"Block {block_dict['index']} added by {email}"}

    def get_chain(self) -> list[dict]:
        return self.chain

    def get_status(self) -> dict:
        return {
            "chain_length": len(self.chain),
            "difficulty": DIFFICULTY,
            "target_prefix": "0" * DIFFICULTY,
            "latest_hash": self.chain[-1]["hash"],
            "ledger": self.ledger,
        }

    def get_latest(self) -> dict:
        return self.chain[-1]

    def get_difficulty(self) -> dict:
        return {"difficulty": DIFFICULTY, "target_prefix": "0" * DIFFICULTY}
