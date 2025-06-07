# setup_ytmusic_oauth.py

from ytmusicapi import setup_oauth
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Get Client ID and Secret
CLIENT_ID = os.getenv("YTMUSIC_CLIENT_ID")
CLIENT_SECRET = os.getenv("YTMUSIC_CLIENT_SECRET")

# Safety check
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing YTMUSIC_CLIENT_ID or YTMUSIC_CLIENT_SECRET in .env!")

# Force save path
SAVE_PATH = "C:/development/music-data-project/oauth.json"

# Run OAuth
print(f"Launching YouTube Music OAuth flow...")
setup_oauth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, filepath=SAVE_PATH)
print(f"OAuth complete! oauth.json created at {SAVE_PATH}")

# Verify
if os.path.exists(SAVE_PATH):
    print("Verified: oauth.json exists!")
else:
    print("ERROR: oauth.json not found — check permissions or try running again.")