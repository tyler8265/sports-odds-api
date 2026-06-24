from fastapi import FastAPI
from enum import Enum
from odds import fetch_odds
from models import Sport, BettingMarkets

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/odds/{sport}/{markets}")
async def get_odds(sport: Sport, markets: list[BettingMarkets]):
  return {"sport": sport, "markets": markets}

