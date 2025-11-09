from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data, save_data, add_user, is_admin
from keyboards import admin_menu, user_menu
from utils import check_subscription, get_subscription_buttons

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Referral tizimi
    if context.args and context.args[0].startswith('ref_'):
        referrer_id = int(context.args[0].split('_')[1])
        data = load_data()
        
        if str(user_id) not in data["users"] and referrer_id != user_id:
            if str(referrer_id) not in data["referrals"]:
                data["referrals"][str(referrer_id)] = []
            data["referrals"][str(referrer_id)].append(user_id)
            
            if len(data["referrals"][str(referrer_id)]) >= 6:
                if referrer_id not in data["vip_users"]:
                    data["vip_users"].append(referrer_id)
            
            save_data(data)
    
    add_user(user_id, username)
    
    # Majburiy obuna tekshirish
    subscribed, not_sub_channels = await check_subscription(context.bot, user_id)
    
    if not subscribed:
        keyboard = await get_subscription_buttons(context.bot, not_sub_channels)
        
        await update.message.reply_text(
            "❗️ Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    if is_admin(user_id):
        await update.message.reply_text(
            "👋 Xush kelibsiz, Admin!\n\nBoshqaruv paneli:",
            reply_markup=admin_menu()
        )
    else:
        await update.message.reply_text(
            "👋 Xush kelibsiz!\n\n🎬 AniVoid botiga xush kelibsiz!",
            reply_markup=user_menu()
        )
