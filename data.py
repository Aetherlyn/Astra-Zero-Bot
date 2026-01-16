import json
from pathlib import Path

DATA_FILE = Path("data.json")

def load_data():
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)
    
def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.data(data, file, indent=2)