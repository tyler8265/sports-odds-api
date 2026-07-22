# Sports Betting Odds Aggregator

A REST API that fetches real-time sports betting odds from multiple bookmakers, normalizes the data, and surfaces the best available line per game. Deployed on AWS EC2 with Docker, automated via GitHub Actions CI/CD, and fronted by a React/Tailwind UI on Vercel.

**Live API:** http://3.133.88.218:8000/docs  
**Frontend:** https://sports-odds-api-bice.vercel.app

---

## What it does

- Fetches live odds from [The Odds API](https://the-odds-api.com) across 80+ sports and leagues
- Compares lines across all available bookmakers and returns the highest payout per game
- Stores a timestamped snapshot of every fetch in SQLite for historical queries
- Exposes a `/history` endpoint to query past odds by team or matchup
- Frontend includes an inline stake calculator — enter a bet amount and it shows payout and profit in real time

---

## Stack

**Backend:** Python, FastAPI, SQLite, httpx  
**Frontend:** React, Tailwind CSS, Vite  
**Infra:** Docker, GitHub Actions, AWS EC2, Vercel

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/odds/{sport}` | Best odds per game for a given sport |
| GET | `/odds/history` | Historical snapshots, filterable by team |
| GET | `/` | Health check |

### Query parameters for `/odds/{sport}`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `region` | string | `us` | Bookmaker region |
| `markets` | list | `h2h` | One or more of: `h2h`, `spreads`, `totals` |

All prices are returned in decimal format.

---

## Running locally

```bash
git clone https://github.com/tyler8265/sports-odds-api
cd sports-odds-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ODDS_API_KEY=your_key_here
```

Get a free API key at [the-odds-api.com](https://the-odds-api.com).

```bash
cd src
uvicorn main:app --reload
```

API runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## Running with Docker

```bash
docker build -t sports-odds-api .
docker run -d -p 8000:8000 --env-file .env sports-odds-api
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`. Set `VITE_API_BASE` in a `.env` file inside `frontend/` if your API is running somewhere other than `/api`.

---

## CI/CD

Every push to `main` triggers a GitHub Actions workflow that:

1. Runs pytest against the API
2. Builds and pushes a Docker image to Docker Hub
3. SSHes into the EC2 instance and restarts the container with the new image

Required GitHub secrets: `ODDS_API_KEY`, `DOCKERHUB_USERNAME`, `DOCKERHUB_PASSWORD`, `EC2_HOST`, `EC2_SSH_KEY`.

---

## Project structure

```
sports-odds-api/
├── src/
│   ├── main.py        # FastAPI app and routes
│   ├── odds.py        # Odds API fetch and best-line logic
│   ├── db.py          # SQLite snapshot storage
│   └── models.py      # Enums for sports, markets, regions
├── tests/
│   └── test_api.py
├── frontend/
│   └── src/
│       └── App.jsx
├── Dockerfile
├── requirements.txt
└── .github/
    └── workflows/
        └── ci-cd-workflow.yml
```
