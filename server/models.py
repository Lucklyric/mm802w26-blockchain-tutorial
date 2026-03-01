from pydantic import BaseModel


class BlockData(BaseModel):
    miner_pubkey: str
    miner_email: str
    action: str


class Block(BaseModel):
    index: int
    timestamp: float
    data: BlockData
    previous_hash: str
    nonce: int
    hash: str
    signature: str


class RegisterRequest(BaseModel):
    pubkey: str
    email: str


class MineRequest(BaseModel):
    index: int
    timestamp: float
    data: BlockData
    previous_hash: str
    nonce: int
    hash: str
    signature: str


class StatusResponse(BaseModel):
    chain_length: int
    difficulty: int
    target_prefix: str
    latest_hash: str
    ledger: dict[str, dict]
