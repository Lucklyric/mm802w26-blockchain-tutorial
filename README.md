# Blockchain Tutorial — Instructor Guide

## Quick Start

```bash
git clone <repo-url>
cd blockchain-tutorial
server/start.sh
```

- Server runs on port 80
- Tutorial: http://<IP>/tutorial/
- Chain Explorer: http://<IP>/tutorial/explorer.html
- API docs: http://<IP>/docs

## GCloud Deployment

1. Create an **e2-micro** instance (Debian/Ubuntu)
2. Install Docker and Docker Compose:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose-plugin
   sudo usermod -aG docker $USER
   # Log out and back in for group change to take effect
   ```
3. Clone the repo and start the server:
   ```bash
   git clone <repo-url>
   cd blockchain-tutorial
   server/start.sh
   ```
4. Open firewall for port 80:
   ```bash
   gcloud compute firewall-rules create allow-http \
     --allow tcp:80 --target-tags http-server
   ```
   Make sure the instance has the `http-server` network tag.

## Student Setup

Students need **Python 3.11+** and **uv** installed locally.

```bash
cd assignment
uv sync
```

Then edit `config.py` with:
- Their email address
- Student random numbers (their choice)
- Instructor random numbers (announced in class)
- Server URL (provided in class)

Follow tutorial steps 1–7.

## Resetting the Chain

Delete all data and restart fresh:

```bash
server/reset.sh
```

## Grading

Visit **http://<IP>/status** to see the ledger, or use the Chain Explorer.

Each student entry shows:
- **status=1**: Block mined and on chain (full credit)
- **block_index**: Which block they mined

## Project Structure

```
├── server/
│   ├── simplechain/          # Blockchain API server
│   │   ├── main.py           # FastAPI app
│   │   ├── blockchain.py     # Chain logic
│   │   ├── crypto_utils.py   # Crypto helpers
│   │   ├── models.py         # Pydantic models
│   │   ├── config.py         # Settings
│   │   └── pyproject.toml    # Python deps
│   ├── tutorial/             # Frontend tutorial + explorer
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── start.sh              # Start server
│   └── reset.sh              # Reset chain + restart
├── assignment/               # Student exercise files
│   ├── config.py             # Student configuration
│   ├── part1_keygen.py       # Key generation exercise
│   ├── part3_explore.py      # Chain exploration exercise
│   ├── part4_create_block.py # Block construction exercise
│   ├── part5_mine.py         # Mining exercise
│   └── part6_submit.py       # Signing + submission exercise
```

## Configuration

- **Difficulty**: Change `DIFFICULTY` in `server/simplechain/config.py` (default: 4)
- **Instructor random numbers**: Announced in class; students enter them in `assignment/config.py`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Student gets "index mismatch" | Someone else mined first — re-run parts 4–6 |
| Student gets "already mined" | They've already completed the assignment |
| Chain gets corrupted | Reset with `server/reset.sh` |
