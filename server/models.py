from pydantic import BaseModel


class BlockData(BaseModel):
    miner_pubkey: str
    miner_email: str
    action: str


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
