import hashlib
import json

from ecdsa import SECP256k1, BadSignatureError, VerifyingKey
from ecdsa.util import sigdecode_der


def compute_block_hash(index: int, timestamp: float, data_dict: dict, previous_hash: str, nonce: int) -> str:
    """Compute SHA256 hash of block contents.

    Hash input format: f"{index}{timestamp}{sorted_data}{previous_hash}{nonce}"
    where sorted_data = json.dumps(data_dict, sort_keys=True)
    """
    sorted_data = json.dumps(data_dict, sort_keys=True)
    block_string = f"{index}{timestamp}{sorted_data}{previous_hash}{nonce}"
    return hashlib.sha256(block_string.encode()).hexdigest()


def verify_signature(pubkey_hex: str, signature_hex: str, message: str) -> bool:
    """Verify ECDSA signature using SECP256k1 curve."""
    try:
        vk = VerifyingKey.from_string(bytes.fromhex(pubkey_hex), curve=SECP256k1)
        vk.verify(bytes.fromhex(signature_hex), message.encode(), hashfunc=hashlib.sha256, sigdecode=sigdecode_der)
        return True
    except (BadSignatureError, Exception):
        return False
