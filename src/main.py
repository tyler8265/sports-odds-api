from fastapi import FastAPI, Query
from odds import fetch_odds
from models import Sport, BettingMarkets, Region
from db import save_snapshot, get_snapshots, init_db
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def db_session(app: FastAPI):
  init_db()
  yield
app = FastAPI(lifespan=db_session)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
  return {"message": "Welcome to Tyler's Sports Betting Odds Aggregator!"}

@app.get("/odds/history")
async def get_history(game: str):
  snapshots = get_snapshots(game)
  return { "historical snapshots": snapshots }

@app.get("/odds/{sport}")
async def get_odds(sport: Sport, region: Region = Region.UNITED_STATES, markets: list[BettingMarkets] = Query(default = [BettingMarkets.MONEYLINE])):
  odds = await fetch_odds(sport, region, markets)
  if odds is None:
    odds = {}
  for game in odds:
    save_snapshot(game, odds.get(game))
  return {"odds": odds}


