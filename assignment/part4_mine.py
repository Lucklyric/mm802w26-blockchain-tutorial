"""
Part 4: Mining (Proof of Work)
===============================
Find a nonce that makes the block hash start with the required number of zeros.

This is the core of Proof of Work: brute-force search for a valid nonce.

The hash is computed as:
    SHA256(f"{index}{timestamp}{json.dumps(data, sort_keys=True)}{previous_hash}{nonce}")

Run: uv run python part4_mine.py
"""
import hashlib
import json
import time
import requests
from config import EMAIL, STUDENT_RANDOM, INSTRUCTOR_RANDOM, SERVER_URL, KEY_FILE
from utils import load_keys, pubkey_hex, display_block
from part3_create_block import create_block


def compute_block_hash(block):
    """
    Compute the SHA256 hash of a block.

    The hash input string format is:
        f"{index}{timestamp}{json.dumps(data, sort_keys=True)}{previous_hash}{nonce}"

    where data is the block's "data" dict.

    Args:
        block: Block dict with index, timestamp, data, previous_hash, nonce

    Returns:
        str: Hex digest of the SHA256 hash
    """
    # === TODO: Compute the block hash ===
    # Hint: Build the string exactly as shown above
    # Hint: hashlib.sha256(block_string.encode()).hexdigest()
    pass


def mine_block(block, difficulty):
    """
    Mine the block by finding a valid nonce.

    Steps:
    1. Start with nonce = 0
    2. Set block["nonce"] = nonce
    3. Compute the hash using compute_block_hash()
    4. If the hash starts with '0' * difficulty, set block["hash"] and return
    5. Otherwise, increment nonce and repeat

    Args:
        block: Block dict (will be modified in place)
        difficulty: Number of leading zeros required

    Returns:
        dict: The mined block with valid nonce and hash
    """
    # === TODO: Implement Proof of Work ===
    # Hint: Use a while loop, incrementing nonce each iteration
    # Hint: Check hash_hex.startswith("0" * difficulty)
    pass


if __name__ == "__main__":
    print("Part 5: Mining")
    print("=" * 40)

    keys = load_keys(KEY_FILE)
    if keys is None:
        print("ERROR: No keys found. Run part1_keygen.py first!")
        exit(1)

    sk, vk = keys
    pub_hex = pubkey_hex(vk)

    # Get difficulty from server
    diff_info = requests.get(f"{SERVER_URL}/difficulty").json()
    difficulty = diff_info["difficulty"]
    print(f"Difficulty: {difficulty} (hash must start with {'0' * difficulty})")

    # Create and mine the block
    block = create_block(SERVER_URL, EMAIL, pub_hex, STUDENT_RANDOM, INSTRUCTOR_RANDOM)
    if block is None:
        print("ERROR: create_block() returned None. Fix Part 4 first!")
        exit(1)

    print(f"\nMining block #{block['index']}...")
    start = time.time()
    mined = mine_block(block, difficulty)
    elapsed = time.time() - start

    if mined is None:
        print("ERROR: mine_block() returned None. Implement the TODO!")
        exit(1)

    print(f"Block mined in {elapsed:.2f} seconds!")
    print(f"Nonce: {mined['nonce']}")
    print(f"Hash: {mined['hash']}")
    display_block(mined)
    print("\nProceed to Part 5 to sign and submit!")
