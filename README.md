# Blockchain Tutorial - Instructor Guide

## Quick Start

```bash
git clone <repo-url>
cd blockchain-tutorial
docker-compose up -d
```

- Server runs on port 80
- Tutorial: http://<IP>/tutorial/
- API: http://<IP>/

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
   docker compose up -d
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
cd client
uv sync
```

Then edit `config.py` with:
- Their email address
- Random numbers announced in class

Follow tutorial steps 1–8.

## Resetting the Chain

Delete all data and restart fresh:

```bash
docker-compose down -v
docker-compose up -d
```

## Grading

Visit **http://<IP>/status** to see the ledger.

Each student entry shows:
- **status=0**: Registered only (partial credit)
- **status=1**: Block mined and on chain (full credit)
- **block_index**: Which block they mined
- Chain timestamps show when each block was mined

## Configuration

- **Difficulty**: Change `DIFFICULTY` in `server/config.py` (default: 4)
- **Instructor random numbers**: Announced in class; students enter them in `client/config.py`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Student gets "index mismatch" | Someone else mined first — re-run parts 4–6 |
| Student gets "already mined" | They've already completed the assignment |
| Chain gets corrupted | Reset with `docker-compose down -v` |
