"""
Part 2: Registration
====================
Register your public key with the blockchain server.

Run: uv run python part2_register.py
"""
import requests
from config import EMAIL, SERVER_URL, KEY_FILE
from utils import load_keys, pubkey_hex


def register(server_url, email, public_key_hex):
    """
    Register your public key with the server.

    Steps:
    1. Send a POST request to {server_url}/register
    2. The JSON body should contain: {"pubkey": public_key_hex, "email": email}
    3. Return the server's JSON response

    Args:
        server_url: Base URL of the blockchain server
        email: Your email address
        public_key_hex: Your public key as a hex string

    Returns:
        dict: Server response
    """
    # === TODO: Send registration request ===
    # Hint: requests.post(url, json={...})
    # Hint: response.json() to get the response body
    pass


if __name__ == "__main__":
    print("Part 2: Registration")
    print("=" * 40)

    keys = load_keys(KEY_FILE)
    if keys is None:
        print("ERROR: No keys found. Run part1_keygen.py first!")
        exit(1)

    sk, vk = keys
    pub_hex = pubkey_hex(vk)
    print(f"Email: {EMAIL}")
    print(f"Public key: {pub_hex[:20]}...")

    result = register(SERVER_URL, EMAIL, pub_hex)
    if result is None:
        print("ERROR: register() returned None. Implement the TODO!")
        exit(1)

    print(f"Server response: {result}")
    print("\nSuccess! Proceed to Part 3.")
