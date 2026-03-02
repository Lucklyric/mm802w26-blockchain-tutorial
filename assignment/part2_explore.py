"""
Part 2: Exploring the Blockchain
=================================
Read the current state of the blockchain using the server's REST API.

Run: uv run python part2_explore.py
"""
import requests
from config import SERVER_URL
from utils import display_block, display_chain_summary


def get_chain(server_url):
    """
    Get the full blockchain.

    Steps:
    1. Send a GET request to {server_url}/chain
    2. Return the JSON response (list of blocks)
    """
    # === TODO: Fetch the blockchain ===
    pass


def get_status(server_url):
    """
    Get the blockchain status (chain length, difficulty, ledger).

    Steps:
    1. Send a GET request to {server_url}/status
    2. Return the JSON response
    """
    # === TODO: Fetch the status ===
    pass


def get_latest_block(server_url):
    """
    Get the latest block in the chain.

    Steps:
    1. Send a GET request to {server_url}/latest
    2. Return the JSON response
    """
    # === TODO: Fetch the latest block ===
    pass


def get_difficulty(server_url):
    """
    Get the current mining difficulty.

    Steps:
    1. Send a GET request to {server_url}/difficulty
    2. Return the JSON response
    """
    # === TODO: Fetch the difficulty ===
    pass


if __name__ == "__main__":
    print("Part 3: Exploring the Blockchain")
    print("=" * 40)

    print("\n--- Chain ---")
    chain = get_chain(SERVER_URL)
    if chain is None:
        print("ERROR: get_chain() returned None. Implement the TODO!")
    else:
        display_chain_summary(chain)

    print("\n--- Status ---")
    status = get_status(SERVER_URL)
    if status is None:
        print("ERROR: get_status() returned None. Implement the TODO!")
    else:
        print(f"Chain length: {status.get('chain_length')}")
        print(f"Difficulty: {status.get('difficulty')}")
        print(f"Latest hash: {status.get('latest_hash', '')[:20]}...")
        print(f"Completed miners: {len(status.get('ledger', {}))}")

    print("\n--- Latest Block ---")
    latest = get_latest_block(SERVER_URL)
    if latest is None:
        print("ERROR: get_latest_block() returned None. Implement the TODO!")
    else:
        display_block(latest)

    print("\n--- Difficulty ---")
    diff = get_difficulty(SERVER_URL)
    if diff is None:
        print("ERROR: get_difficulty() returned None. Implement the TODO!")
    else:
        print(f"Difficulty: {diff.get('difficulty')}")
        print(f"Target prefix: {diff.get('target_prefix')}")

    print("\nDone! Proceed to Part 3.")
