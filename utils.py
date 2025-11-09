from telegram import Bot, InlineKeyboardButton
from database import load_data, is_vip

async def check_subscription(bot: Bot, user_id: int):
    if is_vip(user_id):
        return True, []
    
    data = load_data()
    channels = data["main_channels"] + data["channels"]
    channel_links = data.get("channel_links", [])
    external_links = data.get("external_links", [])
    
    not_subscribed = []
    
    # Storage kanalini tekshirmaydi
    for channel_id in channels:
        if channel_id == -1003124160853:
            continue
            
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status in ['left', 'kicked']:
                not_subscribed.append({"type": "channel", "id": channel_id})
        except:
            continue
    
    # Invite linklar - faqat ko'rsatish uchun (tekshirib bo'lmaydi)
    for link in channel_links:
        not_subscribed.append({"type": "invite_link", "url": link["url"]})
    
    # Tashqi linklar - faqat ko'rsatish
    for link in external_links:
        not_subscribed.append({"type": "external_link", "url": link["url"]})
    
    return len(not_subscribed) == 0, not_subscribed

async def get_subscription_buttons(bot: Bot, not_subscribed: list):
    """Obuna tugmalarini yaratish"""
    keyboard = []
    
    for i, item in enumerate(not_subscribed, 1):
        if item["type"] == "channel":
            channel_id = item["id"]
            try:
                chat = await bot.get_chat(channel_id)
                if chat.username:
                    url = f"https://t.me/{chat.username}"
                else:
                    url = chat.invite_link if hasattr(chat, 'invite_link') else None
                
                if url:
                    keyboard.append([InlineKeyboardButton(f"📢 {chat.title}", url=url)])
            except:
                pass
        
        elif item["type"] == "invite_link":
            keyboard.append([InlineKeyboardButton(f"📢 Telegram kanal #{i}", url=item["url"])])
        
        elif item["type"] == "external_link":
            # URL dan nom olish
            url = item["url"]
            if "instagram.com" in url:
                name = "Instagram"
            elif "youtube.com" in url or "youtu.be" in url:
                name = "YouTube"
            elif "twitter.com" in url or "x.com" in url:
                name = "Twitter/X"
            elif "facebook.com" in url:
                name = "Facebook"
            else:
                name = "Link"
            
            keyboard.append([InlineKeyboardButton(f"🌐 {name}", url=url)])
    
    keyboard.append([InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")])
    
    return keyboard

async def get_channel_link(bot: Bot, channel_id):
    try:
        chat = await bot.get_chat(channel_id)
        if chat.username:
            return f"https://t.me/{chat.username}"
        else:
            return chat.invite_link if hasattr(chat, 'invite_link') else None
    except:
        return None

async def get_channel_name(bot: Bot, channel_id):
    try:
        chat = await bot.get_chat(channel_id)
        return chat.title
    except:
        return f"Kanal"

def generate_referral_link(bot_username, user_id):
    return f"https://t.me/{bot_username}?start=ref_{user_id}"
