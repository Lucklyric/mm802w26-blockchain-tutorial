from pydantic import BaseModel


class BlockData(BaseModel):
    miner_pubkey: str
    miner_email: str
    student_random: list[int]
    instructor_random: list[int]
    action: str


class MineRequest(BaseModel):
    index: int
    timestamp: float
    data: BlockData
    previous_hash: str
    nonce: int
    hash: str
    signature: str
