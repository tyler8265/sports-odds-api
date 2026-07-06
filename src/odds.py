import httpx
import os
import asyncio
from models import Sport, Region, BettingMarkets
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4"

###all winnings are based off of a 1.00 bet, so the winnings shown can just be used as a multiplier
def calculate_winnings(bet: float, multiplier: float):
  if bet > 0.0:
    return bet * multiplier
  else:
    print("Not an acceptable bet. Please place a bet above 0.")
    return 0.0

##the goal is to find the best sportsbook odds per game
async def fetch_odds(sport: Sport, regions: Region = Region.UNITED_STATES, markets: list[BettingMarkets] | None = None):
  async with httpx.AsyncClient() as client:
    try:
      if markets is None:
        markets = [BettingMarkets.MONEYLINE]
      sport = sport.value
      regions = regions.value
      markets = [m.value for m in markets]
      res = await client.get(f"{BASE_URL}/sports/{sport}/odds/", params={"apiKey": API_KEY, "regions": regions, "markets": ','.join(markets), "oddsFormat": "decimal"})
      data = res.json()
      if data is None:
        data = {}
      odds_per_game = {}
      for game in data:
        list_of_outcomes = []
        for i in range(len(game['bookmakers'])):
          j = 0
          while j < len(game['bookmakers'][i]['markets']):
            if game['bookmakers'][i]['markets'][j].get('key') in markets:
              list_of_outcomes.append((
                game['bookmakers'][i]['title'],
                game['bookmakers'][i]['markets'][j].get('key'),
                game['bookmakers'][i]['markets'][j].get('outcomes'),
                game['sport_key']
              ))
            j+=1
        odds_per_game[f"{game.get('home_team')}" + ' vs ' + f"{game.get('away_team')}" + ' at ' + f"{game.get('commence_time')}"] = list_of_outcomes
      best_odds_per_game = {}
      for game in odds_per_game.keys():
        best_per_market = {}
        for i in range(len(odds_per_game[game])):
          market_key = odds_per_game[game][i][1]
          for j in range(len(odds_per_game[game][i][2])):
            price = odds_per_game[game][i][2][j].get('price')
            current_best = best_per_market.get(market_key, {}).get('price', 0)
            if price and price > current_best:
              best_per_market[market_key] = {'price': price, 'index': i, 'inner': j}
        for market_key, best in best_per_market.items():
          i = best['index']
          j = best['inner']
          best_odds_per_game[f"{game}___{market_key}"] = (odds_per_game[game][i][0], odds_per_game[game][i][3],
                                                          market_key, odds_per_game[game][i][2][j])
      return best_odds_per_game
    except Exception as e:
      import traceback
      traceback.print_exc()
      print(f"Error: {e}")

