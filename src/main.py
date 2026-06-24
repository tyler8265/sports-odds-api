from fastapi import FastAPI
from odds import fetch_odds
from models import Sport, BettingMarkets, Region

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/odds/{sport}")
async def get_odds(sport: Sport, region: Region, markets: list[BettingMarkets] = [BettingMarkets.MONEYLINE]):
  odds = await fetch_odds(sport, region, markets)
  return {"odds": odds}

