import json
import os
from config import DATA_FILE, ADMIN_ID

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "owner": ADMIN_ID,
        "admins": [],
        "users": {},
        "vip_users": [],
        "animes": {},
        "hentai": {},
        "main_channels": [],
        "channels": [],
        "vip_message": "",
        "contact_message": "",
        "referrals": {}
    }

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_owner(user_id):
    data = load_data()
    return user_id == data["owner"]

def is_admin(user_id):
    data = load_data()
    return user_id == data["owner"] or user_id in data["admins"]

def add_user(user_id, username):
    data = load_data()
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {
            "username": username,
            "active": True,
            "referrals": 0
        }
        save_data(data)

def is_vip(user_id):
    data = load_data()
    return user_id in data["vip_users"]

def get_stats():
    data = load_data()
    total = len(data["users"])
    active = sum(1 for u in data["users"].values() if u.get("active", True))
    inactive = total - active
    vip = len(data["vip_users"])
    animes = len(data["animes"])
    hentai = len(data["hentai"])
    return f"📊 Statistika:\n\n👥 Foydalanuvchilar - {total}\n✅ Active - {active}\n❌ Unactive - {inactive}\n⭐ Vip - {vip}\n🎬 Animelar - {animes}\n🔞 Hentailar - {hentai}"
