from telegram import Update
from telegram.ext import ContextTypes
from database import is_admin
from keyboards import admin_menu, user_menu
from utils import check_subscription

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    # Majburiy obuna
    if data == "check_sub":
        subscribed, _ = await check_subscription(context.bot, user_id)
        if subscribed:
            await query.answer("✅ Obuna tasdiqlandi!")
            if is_admin(user_id):
                await query.message.reply_text("👋 Xush kelibsiz, Admin!", reply_markup=admin_menu())
            else:
                await query.message.reply_text("👋 Xush kelibsiz!", reply_markup=user_menu())
        else:
            await query.answer("❌ Barcha kanallarga obuna bo'ling!", show_alert=True)
        return
    
    # Menu
    elif data == "admin_menu":
        await query.answer()
        await query.message.reply_text("🔧 Boshqaruv paneli:", reply_markup=admin_menu())
        return
    
    elif data == "user_menu":
        await query.answer()
        await query.message.reply_text("🏠 Asosiy menu:", reply_markup=user_menu())
        return
    
    # Tasdiqlash (yangi anime)
    elif data == "confirm_episodes":
        from handlers.admin.anime_add import handle_confirm_episodes
        await handle_confirm_episodes(update, context)
        return
    
    # Yangi qismlarni tasdiqlash
    elif data.startswith("confirm_new_episodes_"):
        anime_id = data.split("_")[-1]
        from handlers.admin.ongoing import handle_confirm_new_episodes
        await handle_confirm_new_episodes(update, context, anime_id)
        return
    
    # Kanalga yuborish
    elif data.startswith("send_to_channel_"):
        anime_id = data.split("_")[-1]
        from handlers.admin.ongoing import handle_send_to_channel
        await handle_send_to_channel(update, context, anime_id)
        return
    
    # Bekor qilish
    elif data == "cancel_episodes":
        await query.answer()
        from handlers.admin_panel import user_states
        if user_id in user_states:
            del user_states[user_id]
        await query.message.reply_text("❌ Bekor qilindi", reply_markup=admin_menu())
        return
    
    # Reklama yuborish
    elif data == "send_broadcast":
        from handlers.admin.broadcast import send_broadcast
        await send_broadcast(update, context)
        return
    
    # Ongoing
    elif data == "ongoing":
        from handlers.admin.ongoing import handle_ongoing
        await handle_ongoing(update, context, page=1)
        return
    
    # Yangi anime yuborish
    elif data == "send_new_anime":
        from handlers.admin.anime_add import handle_send_new_anime
        await handle_send_new_anime(update, context)
        return
