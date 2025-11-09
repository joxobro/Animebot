from telegram import Update
from telegram.ext import ContextTypes
from database import load_data, is_vip
from config import STORAGE_CHANNEL

async def handle_watch_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return
    
    param = context.args[0]
    user_id = update.effective_user.id
    
    # Anime tomosha qilish
    if param.startswith('watch_') or param.startswith('watchh_'):
        is_hentai = param.startswith('watchh_')
        anime_id = param.split('_')[1]
        
        data = load_data()
        
        # Hentai uchun VIP tekshirish
        if is_hentai:
            if not is_vip(user_id):
                await update.message.reply_text("❌ Bu kontent faqat VIP foydalanuvchilar uchun!")
                return
            anime_dict = data["hentai"]
        else:
            anime_dict = data["animes"]
        
        if anime_id not in anime_dict:
            await update.message.reply_text("❌ Anime topilmadi!")
            return
        
        anime_info = anime_dict[anime_id]
        
        # Postni yuborish
        try:
            await context.bot.copy_message(
                chat_id=user_id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=anime_info["post_id"]
            )
        except:
            pass
        
        # Qismlarni yuborish
        for episode_id in anime_info["episodes"]:
            try:
                await context.bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=STORAGE_CHANNEL,
                    message_id=episode_id
                )
            except Exception as e:
                print(f"Qism yuborishda xato: {e}")
        
        # Kanal username
        main_channels = data.get("main_channels", [])
        if main_channels:
            try:
                chat = await context.bot.get_chat(main_channels[0])
                if chat.username:
                    await update.message.reply_text(f"📺 Kanal - @{chat.username}")
                else:
                    await update.message.reply_text(f"📺 Kanal - {chat.title}")
            except:
                pass
