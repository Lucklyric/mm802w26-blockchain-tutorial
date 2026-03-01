import json
import os
from ecdsa import SigningKey, SECP256k1


def load_keys(key_file):
    """Load signing key and verifying key from file.

    Returns:
        tuple: (SigningKey, VerifyingKey) or None if file doesn't exist
    """
    if not os.path.exists(key_file):
        return None
    with open(key_file, "r") as f:
        lines = f.read().strip().split("\n")
    sk_hex = lines[0]
    sk = SigningKey.from_string(bytes.fromhex(sk_hex), curve=SECP256k1)
    vk = sk.get_verifying_key()
    return sk, vk


def save_keys(signing_key, verifying_key, key_file):
    """Save keys to file as hex strings (one per line: sk_hex then vk_hex)."""
    sk_hex = signing_key.to_string().hex()
    vk_hex = verifying_key.to_string().hex()
    with open(key_file, "w") as f:
        f.write(f"{sk_hex}\n{vk_hex}\n")


def pubkey_hex(verifying_key):
    """Return hex string of verifying key bytes."""
    return verifying_key.to_string().hex()


def display_block(block):
    """Pretty-print a block dict."""
    print(json.dumps(block, indent=2))


def display_chain_summary(chain):
    """Print chain length and each block's index, miner_email, hash (truncated)."""
    print(f"Chain length: {len(chain)}")
    for block in chain:
        index = block.get("index", "?")
        data = block.get("data", {})
        miner = data.get("miner_email", "genesis")
        block_hash = block.get("hash", "")[:20]
        print(f"  Block #{index} | miner: {miner} | hash: {block_hash}...")
