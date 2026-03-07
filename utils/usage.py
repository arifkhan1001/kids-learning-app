import json
import os
from datetime import datetime

USAGE_FILE = "usage.json"
DAILY_LIMIT = 1500

def get_usage():
    if not os.path.exists(USAGE_FILE):
        return {"date": datetime.now().strftime("%Y-%m-%d"), "used": 0}
    
    try:
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
            
        today = datetime.now().strftime("%Y-%m-%d")
        if data.get("date") != today:
            # Reset usage for a new day
            data = {"date": today, "used": 0}
            _save_usage(data)
            
        return data
    except Exception:
        return {"date": datetime.now().strftime("%Y-%m-%d"), "used": 0}

def _save_usage(data):
    try:
        with open(USAGE_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

def increment_usage(amount=1):
    data = get_usage()
    data["used"] += amount
    _save_usage(data)
    return data

def get_remaining():
    data = get_usage()
    return max(0, DAILY_LIMIT - data["used"])
