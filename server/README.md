# Server

## Quick Start

```bash
server/start.sh
```

- Tutorial: http://<IP>/tutorial/
- Chain Explorer: http://<IP>/tutorial/explorer.html
- API docs: http://<IP>/docs

## GCloud Deployment

1. Create an **e2-micro** instance (Debian/Ubuntu)
2. Install Docker:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose-plugin
   sudo usermod -aG docker $USER
   # Log out and back in
   ```
3. Clone and start:
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

## Reset Chain

```bash
server/reset.sh
```

## Grading

Visit `/status` or the Chain Explorer. Each student: **status=1** = full credit.

## Configuration

- **Difficulty**: `server/simplechain/config.py` (default: 4)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "index mismatch" | Someone mined first — re-run parts 4–6 |
| "already mined" | Already completed |
| Chain corrupted | `server/reset.sh` |
