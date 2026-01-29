import sqlite3
from pathlib import Path

DB_PATH = Path("data/astra.db")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# === Data Base ===

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                
                name TEXT DEFAULT 'Unnamed',
                race TEXT DEFAULT 'Unknown',
                class_and_level TEXT DEFAULT 'Unknown',
                     
                hp INTEGER DEFAULT 0,
                ac INTEGER DEFAULT 0,
                speed INTEGER DEFAULT 30,
                
                strength INTEGER DEFAULT 10,
                dexterity INTEGER DEFAULT 10,
                constitution INTEGER DEFAULT 10,
                intelligence INTEGER DEFAULT 10,
                wisdom INTEGER DEFAULT 10,
                charisma INTEGER DEFAULT 10,
                
                proficiency_bonus INTEGER DEFAULT 2,
                initiative INTEGER DEFAULT 0,
                inspiration INTEGER NOT NULL DEFAULT 0,

                     
                tools TEXT DEFAULT '',
                languages TEXT DEFAULT '',
                     
                UNIQUE (guild_id, user_id)
            )
        """)

# === Commmands ===

def get_or_create_character(guild_id: int, user_id: int):
    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM characters WHERE guild_id=? AND user_id=?", (guild_id, user_id))
        row = cur.fetchone()

        if row:
            return row
        else:
            cur.execute("INSERT INTO characters (guild_id, user_id) VALUES (?, ?)", (guild_id, user_id))
            conn.commit()

            return cur.execute("SELECT * FROM characters WHERE guild_id=? AND user_id=?", (guild_id, user_id)).fetchone()
    
def update_character_field(guild_id, user_id, field, value):
    allowed_fields = {
        "name","race","class_and_level","hp","ac","speed","strength","dexterity","constitution","intelligence","wisdom","charisma","proficiency_bonus","initiative","tools","languages","inspiration"
    }

    if field not in allowed_fields:
        raise ValueError("Invalid field")
    
    with get_conn() as conn:
        conn.execute(f"UPDATE characters SET {field}=? WHERE guild_id=? AND user_id=?",(value, guild_id, user_id))
        conn.commit()