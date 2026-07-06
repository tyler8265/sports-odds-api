import psycopg2
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

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
    curr_time = datetime.now(timezone.utc).isoformat()
    data = json.dumps(odds_data)
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO snapshots(sport, game, data, fetched_at) VALUES (%s, %s, %s, %s);",
                (odds_data[1], game, data, curr_time)
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
