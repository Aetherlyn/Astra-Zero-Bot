import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

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
                class TEXT DEFAULT 'Unknown',
                     
                hp INTEGER NOT NULL DEFAULT 0,
                current_hp INTEGER NOT NULL DEFAULT 0,
                temp_hp INTEGER NOT NULL DEFAULT 0,
                max_hp_bonus INTEGER NOT NULL DEFAULT 0,
                          
                ac INTEGER NOT NULL DEFAULT 0,
                speed INTEGER NOT NULL DEFAULT 30,
                
                strength INTEGER NOT NULL DEFAULT 10,
                dexterity INTEGER NOT NULL DEFAULT 10,
                constitution INTEGER NOT NULL DEFAULT 10,
                intelligence INTEGER NOT NULL DEFAULT 10,
                wisdom INTEGER NOT NULL DEFAULT 10,
                charisma INTEGER NOT NULL DEFAULT 10,
                
                proficiency INTEGER NOT NULL DEFAULT 2,
                initiative INTEGER NOT NULL DEFAULT 0,
                inspiration INTEGER NOT NULL DEFAULT 0,
                exhaustion INTEGER NOT NULL DEFAULT 0,

                weapons TEXT DEFAULT '',
                armor TEXT DEFAULT '',     
                tools TEXT DEFAULT '',
                languages TEXT DEFAULT '',
                     
                hd_d6 INTEGER NOT NULL DEFAULT 0,
                current_hd_d6 INTEGER NOT NULL DEFAULT 0,
                hd_d8 INTEGER NOT NULL DEFAULT 0,
                current_hd_d8 INTEGER NOT NULL DEFAULT 0,
                hd_d10 INTEGER NOT NULL DEFAULT 0,
                current_hd_d10 INTEGER NOT NULL DEFAULT 0,
                hd_d12 INTEGER NOT NULL DEFAULT 0,
                current_hd_d12 INTEGER NOT NULL DEFAULT 0,
                     
                athletics_prof INTEGER NOT NULL DEFAULT 0,
                acrobatics_prof INTEGER NOT NULL DEFAULT 0,
                sleight_of_hand_prof INTEGER NOT NULL DEFAULT 0,
                stealth_prof INTEGER NOT NULL DEFAULT 0,
                arcana_prof INTEGER NOT NULL DEFAULT 0,
                history_prof INTEGER NOT NULL DEFAULT 0,
                investigation_prof INTEGER NOT NULL DEFAULT 0,
                nature_prof INTEGER NOT NULL DEFAULT 0,
                religion_prof INTEGER NOT NULL DEFAULT 0,
                animal_handling_prof INTEGER NOT NULL DEFAULT 0,
                insight_prof INTEGER NOT NULL DEFAULT 0,
                medicine_prof INTEGER NOT NULL DEFAULT 0,
                perception_prof INTEGER NOT NULL DEFAULT 0,
                survival_prof INTEGER NOT NULL DEFAULT 0,
                deception_prof INTEGER NOT NULL DEFAULT 0,
                intimidation_prof INTEGER NOT NULL DEFAULT 0,
                performance_prof INTEGER NOT NULL DEFAULT 0,
                persuasion_prof INTEGER NOT NULL DEFAULT 0,
                        
                UNIQUE (guild_id, user_id)
            )
        """)

# === Commmands ===

def create_character(guild_id: int, user_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO characters (guild_id, user_id) VALUES(?, ?)", (guild_id, user_id))
        conn.commit()

        return cur.execute("SELECT * FROM characters WHERE guild_id=? AND user_id=?",(guild_id, user_id)).fetchone()
    
def read_character(guild_id: int, user_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM characters WHERE guild_id=? AND user_id=?",(guild_id, user_id))

        return cur.fetchone()
    
def write_character(guild_id, user_id, field, value):
    allowed_fields = {
        "name","race","class","hp","current_hp","temp_hp","max_hp_bonus","ac","speed","strength","dexterity","constitution","intelligence","wisdom","charisma","proficiency","initiative","weapons","armor","tools","languages","inspiration","hd_d6",
        "current_hd_d6","hd_d8","current_hd_d8","hd_d10","current_hd_d10","hd_d12","current_hd_d12","exhaustion"
    }

    if field not in allowed_fields:
        logger.error("Attempted to update invalid field: %s", field)
        raise ValueError("Invalid field")
    
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE characters SET {field}=? WHERE guild_id=? AND user_id=?",(value, guild_id, user_id))
        conn.commit()