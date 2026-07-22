import psycopg2
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL.strip())

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS snapshots(
                    id SERIAL PRIMARY KEY,
                    sport TEXT NOT NULL,
                    game TEXT NOT NULL,
                    data TEXT NOT NULL,
                    fetched_at TEXT NOT NULL
                )
            """)
        conn.commit()


def save_snapshot(game, odds_data):
  curr_time = datetime.now(timezone.utc)
  with get_conn() as conn:
    with conn.cursor() as cursor:
      cursor.execute(
        "SELECT fetched_at FROM snapshots WHERE game = %s ORDER BY fetched_at DESC LIMIT 1",
        (game,)
      )
      row = cursor.fetchone()
      if row:
        last_fetch = datetime.fromisoformat(row[0])
        if last_fetch.tzinfo is None:
          last_fetch = last_fetch.replace(tzinfo=timezone.utc)
        if (curr_time - last_fetch).total_seconds() < 1800:
          return
    data = json.dumps([bet.model_dump() for bet in odds_data])
    with conn.cursor() as cursor:
      cursor.execute(
        "INSERT INTO snapshots(sport, game, data, fetched_at) VALUES (%s, %s, %s, %s);",
        (odds_data[0].sport, game, data, curr_time.isoformat())
      )
    conn.commit()

def get_snapshots(game=None):
    snapshots = []
    with get_conn() as conn:
        with conn.cursor() as cursor:
            if game:
                cursor.execute("SELECT * FROM snapshots WHERE game LIKE %s", (f"%{game}%",))
            else:
                cursor.execute("SELECT * FROM snapshots")
            rows = cursor.fetchall()
            for row in rows:
                row = list(row)
                row[3] = json.loads(row[3])
                snapshots.append(row)
    return snapshots


def get_distinct_games(sport=None):
  with get_conn() as conn:
    with conn.cursor() as cursor:
      if sport:
        cursor.execute("SELECT DISTINCT game FROM snapshots WHERE sport = %s ORDER BY game", (sport,))
      else:
        cursor.execute("SELECT DISTINCT game FROM snapshots ORDER BY game")
      rows = cursor.fetchall()
      return [row[0] for row in rows]
