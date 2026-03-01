"""
Part 1: Key Generation
======================
Generate a deterministic ECDSA key pair from your personal seed.

Your seed is: SHA256(email + student_random_numbers + instructor_random_numbers)
This seed is used to generate a secp256k1 ECDSA key pair (same curve as Bitcoin).

Run: uv run python part1_keygen.py
"""
import hashlib
import json
from ecdsa import SigningKey, SECP256k1
from config import EMAIL, STUDENT_RANDOM, INSTRUCTOR_RANDOM, KEY_FILE
from utils import save_keys, pubkey_hex


def generate_seed():
    """
    Generate a deterministic seed from your email and random numbers.

    Steps:
    1. Create a string by concatenating: EMAIL + str(STUDENT_RANDOM) + str(INSTRUCTOR_RANDOM)
    2. Hash it with SHA256
    3. Return the raw bytes (digest, not hexdigest)

    Returns:
        bytes: 32-byte SHA256 hash to use as seed
    """
    # === TODO: Implement seed generation ===
    # Hint: Use hashlib.sha256(...).digest()
    # Hint: The input string should be: EMAIL + str(STUDENT_RANDOM) + str(INSTRUCTOR_RANDOM)
    pass


def generate_keypair(seed_bytes):
    """
    Generate an ECDSA key pair from the seed bytes.

    Steps:
    1. Create a SigningKey from the seed bytes using SECP256k1 curve
    2. Get the VerifyingKey from the SigningKey

    Args:
        seed_bytes: 32 bytes to use as the private key seed

    Returns:
        tuple: (SigningKey, VerifyingKey)
    """
    # === TODO: Generate ECDSA key pair ===
    # Hint: SigningKey.from_string(seed_bytes, curve=SECP256k1)
    # Hint: signing_key.get_verifying_key()
    pass


if __name__ == "__main__":
    print("Part 1: Key Generation")
    print("=" * 40)

    seed = generate_seed()
    if seed is None:
        print("ERROR: generate_seed() returned None. Implement the TODO!")
        exit(1)

    print(f"Seed (hex): {seed.hex()}")
    print(f"Seed length: {len(seed)} bytes")

    sk, vk = generate_keypair(seed)
    if sk is None:
        print("ERROR: generate_keypair() returned None. Implement the TODO!")
        exit(1)

    print(f"Public key: {pubkey_hex(vk)}")
    save_keys(sk, vk, KEY_FILE)
    print(f"Keys saved to {KEY_FILE}")
    print("\nSuccess! Proceed to Part 2.")
