from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from blockchain import Blockchain
from models import MineRequest, RegisterRequest

app = FastAPI(title="Blockchain Tutorial Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bc = Blockchain()

tutorial_dir = Path(__file__).parent / "tutorial"
if not tutorial_dir.exists():
    tutorial_dir = Path(__file__).parent.parent / "tutorial"
if tutorial_dir.exists():
    app.mount("/tutorial", StaticFiles(directory=str(tutorial_dir), html=True), name="tutorial")


@app.get("/")
def root():
    return {"message": "Blockchain Tutorial Server", "docs": "/docs"}


@app.get("/chain")
def get_chain():
    return bc.get_chain()


@app.get("/status")
def get_status():
    return bc.get_status()


@app.get("/latest")
def get_latest():
    return bc.get_latest()


@app.get("/difficulty")
def get_difficulty():
    return bc.get_difficulty()


@app.post("/register")
def register(request: RegisterRequest):
    return bc.register(request.pubkey, request.email)


@app.post("/mine")
def mine(request: MineRequest):
    block_dict = request.model_dump()
    block_dict["data"] = dict(block_dict["data"])
    return bc.submit_block(block_dict)


if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT

    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
