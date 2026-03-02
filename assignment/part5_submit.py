"""
Part 5: Signing and Submitting
===============================
Sign your mined block and submit it to the blockchain.

Run: uv run python part5_submit.py
"""
import hashlib
import json
import time
import requests
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der
from config import EMAIL, STUDENT_RANDOM, INSTRUCTOR_RANDOM, SERVER_URL, KEY_FILE
from utils import load_keys, pubkey_hex, display_block
from part3_create_block import create_block
from part4_mine import mine_block, compute_block_hash


def sign_block(signing_key, block_hash):
    """
    Sign the block hash with your private key.

    Steps:
    1. Sign the block_hash string using the signing_key
    2. Use SHA256 as the hash function and DER encoding
    3. Return the signature as a hex string

    Args:
        signing_key: Your ECDSA SigningKey
        block_hash: The block's hash string to sign

    Returns:
        str: DER-encoded signature as hex string
    """
    # === TODO: Sign the block hash ===
    # Hint: signing_key.sign(data, hashfunc=hashlib.sha256, sigencode=sigencode_der)
    # Hint: The data to sign is block_hash.encode()
    # Hint: Return signature.hex()
    pass


def submit_block(server_url, block):
    """
    Submit the mined and signed block to the server.

    Steps:
    1. Send a POST request to {server_url}/mine
    2. The JSON body should be the entire block dict
    3. Return the server's JSON response

    Args:
        server_url: Base URL of the blockchain server
        block: Complete block dict with valid hash and signature

    Returns:
        dict: Server response
    """
    # === TODO: Submit the block ===
    # Hint: requests.post(url, json=block)
    pass


if __name__ == "__main__":
    print("Part 6: Sign and Submit")
    print("=" * 40)

    keys = load_keys(KEY_FILE)
    if keys is None:
        print("ERROR: No keys found. Run part1_keygen.py first!")
        exit(1)

    sk, vk = keys
    pub_hex = pubkey_hex(vk)

    # Get difficulty
    diff_info = requests.get(f"{SERVER_URL}/difficulty").json()
    difficulty = diff_info["difficulty"]

    # Create block
    block = create_block(SERVER_URL, EMAIL, pub_hex, STUDENT_RANDOM, INSTRUCTOR_RANDOM)
    if block is None:
        print("ERROR: Fix Part 4 first!")
        exit(1)

    # Mine block
    print(f"Mining block #{block['index']} (difficulty={difficulty})...")
    start = time.time()
    mined = mine_block(block, difficulty)
    elapsed = time.time() - start
    if mined is None:
        print("ERROR: Fix Part 5 first!")
        exit(1)
    print(f"Mined in {elapsed:.2f}s (nonce={mined['nonce']})")

    # Sign block
    signature = sign_block(sk, mined["hash"])
    if signature is None:
        print("ERROR: sign_block() returned None. Implement the TODO!")
        exit(1)
    mined["signature"] = signature
    print(f"Signature: {signature[:40]}...")

    # Submit block
    print("\nSubmitting block...")
    result = submit_block(SERVER_URL, mined)
    if result is None:
        print("ERROR: submit_block() returned None. Implement the TODO!")
        exit(1)
    print(f"Server response: {result}")

    # Verify
    print("\nVerifying...")
    status = requests.get(f"{SERVER_URL}/status").json()
    ledger = status.get("ledger", {})
    if EMAIL in ledger and ledger[EMAIL].get("status") == 1:
        print(f"SUCCESS! Your block is on the chain. Status: DONE")
    else:
        print("Block not yet confirmed. Check the error message above.")
