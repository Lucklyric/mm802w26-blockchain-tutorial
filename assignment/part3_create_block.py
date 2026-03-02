"""
Part 3: Creating a Block
=========================
Construct a valid block structure that's ready for mining.

Run: uv run python part3_create_block.py
"""
import time
import requests
from config import EMAIL, STUDENT_RANDOM, INSTRUCTOR_RANDOM, SERVER_URL, KEY_FILE
from utils import load_keys, pubkey_hex, display_block


def create_block(server_url, email, public_key_hex, student_random, instructor_random):
    """
    Create a new block structure ready for mining.

    Steps:
    1. GET /latest from the server to find the previous block
    2. Build a block dict with these fields:
       - "index": previous block's index + 1
       - "timestamp": current time (use time.time())
       - "data": {
             "miner_pubkey": public_key_hex,
             "miner_email": email,
             "student_random": student_random,
             "instructor_random": instructor_random,
             "action": "set_done"
         }
       - "previous_hash": the hash of the latest block
       - "nonce": 0  (placeholder, will be changed during mining)
       - "hash": ""  (placeholder, will be computed during mining)
       - "signature": ""  (placeholder, will be added after mining)

    Args:
        server_url: Base URL of the blockchain server
        email: Your email address
        public_key_hex: Your public key as hex string
        student_random: Your random numbers (list of ints)
        instructor_random: Instructor's random numbers (list of ints)

    Returns:
        dict: Block structure ready for mining
    """
    # === TODO: Create block structure ===
    # Hint: First fetch the latest block to get its hash and index
    # Hint: requests.get(f"{server_url}/latest").json()
    # Hint: The data dict must include student_random and instructor_random
    pass


if __name__ == "__main__":
    print("Part 4: Creating a Block")
    print("=" * 40)

    keys = load_keys(KEY_FILE)
    if keys is None:
        print("ERROR: No keys found. Run part1_keygen.py first!")
        exit(1)

    sk, vk = keys
    pub_hex = pubkey_hex(vk)

    block = create_block(SERVER_URL, EMAIL, pub_hex, STUDENT_RANDOM, INSTRUCTOR_RANDOM)
    if block is None:
        print("ERROR: create_block() returned None. Implement the TODO!")
        exit(1)

    print("Block created:")
    display_block(block)
    print("\nNote: nonce, hash, and signature are placeholders.")
    print("Proceed to Part 4 to mine the block!")
