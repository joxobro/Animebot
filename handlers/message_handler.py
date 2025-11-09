from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data, save_data, is_admin, get_stats
from keyboards import admin_menu, user_menu
from config import STORAGE_CHANNEL

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    text = update.message.text
    
    # Import handlers
    from handlers.admin.ongoing import handle_anime_selected
    from handlers.admin.broadcast import start_broadcast, handle_broadcast_message
    from handlers.admin_panel import user_states
    
    # ==================== ADMIN TUGMALAR ====================
    
    # Anime qo'shish
    if text == "➕ Anime qo'shish":
        user_states[user_id] = {"state": "waiting_anime_name", "is_hentai": False}
        await update.message.reply_text("📝 Anime nomini kiriting:")
        return
    
    # Hentai
    elif text == "🔞 Hentai":
        user_states[user_id] = {"state": "waiting_anime_name", "is_hentai": True}
        await update.message.reply_text("📝 Hentai nomini kiriting:")
        return
    
    # Statistika
    elif text == "📊 Statistika":
        stats = get_stats()
        await update.message.reply_text(stats, reply_markup=admin_menu())
        return
    
    # Ongoing
    elif text == "📺 Ongoing":
        from handlers.admin.ongoing import handle_ongoing
        await handle_ongoing(update, context)
        return
    
    # Reklama
    elif text == "📢 Reklama":
        await start_broadcast(update, context)
        return
    
    # Admin
    elif text == "👤 Admin":
        if is_admin(user_id):
            data = load_data()
            admins = data.get("admins", [])
            
            admin_text = "👤 Adminlar:\n\n"
            if not admins:
                admin_text += "Hozircha adminlar yo'q\n"
            else:
                for i, admin_id in enumerate(admins, 1):
                    admin_text += f"{i}. ID: {admin_id}\n"
            
            admin_text += "\n📝 Admin qo'shish uchun ID yuboring\n📝 Admin o'chirish uchun ID ni qayta yuboring"
            
            await update.message.reply_text(admin_text)
            user_states[user_id] = {"state": "waiting_admin_action"}
        return
    
    # Kanal
    elif text == "📱 Kanal":
        if is_admin(user_id):
            keyboard = [
                [KeyboardButton("✅ Asosiy kanal")],
                [KeyboardButton("📱 Kanallar")],
                [KeyboardButton("🔙 Orqaga")]
            ]
            await update.message.reply_text(
                "📱 Kanal sozlamalari:",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
        return
    
    # Asosiy kanal
    elif text == "✅ Asosiy kanal":
        if is_admin(user_id):
            data = load_data()
            main_channels = data.get("main_channels", [])
            
            channel_text = "✅ Asosiy kanallar:\n\n"
            if not main_channels:
                channel_text += "Hozircha asosiy kanal yo'q\n"
            else:
                for i, ch_id in enumerate(main_channels, 1):
                    channel_text += f"{i}. ID: {ch_id}\n"
            
            channel_text += "\n📝 Kanal qo'shish uchun kanal ID yuboring (masalan: -1001234567890)\n📝 Kanal o'chirish uchun ID ni qayta yuboring"
            
            await update.message.reply_text(channel_text)
            user_states[user_id] = {"state": "waiting_main_channel"}
        return
    
    # Kanallar
    elif text == "📱 Kanallar":
        if is_admin(user_id):
            data = load_data()
            channels = data.get("channels", [])
            
            channel_text = "📱 Majburiy obuna kanallari:\n\n"
            if not channels:
                channel_text += "Hozircha kanallar yo'q\n"
            else:
                for i, ch_id in enumerate(channels, 1):
                    channel_text += f"{i}. ID: {ch_id}\n"
            
            channel_text += "\n📝 Kanal qo'shish uchun kanal ID yuboring (masalan: -1001234567890)\n📝 Kanal o'chirish uchun ID ni qayta yuboring"
            
            await update.message.reply_text(channel_text)
            user_states[user_id] = {"state": "waiting_channel"}
        return
    
    # Sozlamalar
    elif text == "⚙️ Sozlamalar":
        if is_admin(user_id):
            keyboard = [
                [KeyboardButton("⭐ Vip xabar")],
                [KeyboardButton("📞 Bog'lanish xabar")],
                [KeyboardButton("🔙 Orqaga")]
            ]
            await update.message.reply_text(
                "⚙️ Sozlamalar:",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
        return
    
    # Vip xabar
    elif text == "⭐ Vip xabar":
        if is_admin(user_id):
            data = load_data()
            current_msg = data.get("vip_message", "")
            
            if current_msg:
                await update.message.reply_text(f"📝 Joriy xabar:\n\n{current_msg}\n\n📝 Yangi xabar yuboring:")
            else:
                await update.message.reply_text("📝 VIP uchun xabar yuboring:")
            
            user_states[user_id] = {"state": "waiting_vip_message"}
        return
    
    # Bog'lanish xabar
    elif text == "📞 Bog'lanish xabar":
        if is_admin(user_id):
            data = load_data()
            current_msg = data.get("contact_message", "")
            
            if current_msg:
                await update.message.reply_text(f"📝 Joriy xabar:\n\n{current_msg}\n\n📝 Yangi xabar yuboring:")
            else:
                await update.message.reply_text("📝 Bog'lanish uchun xabar yuboring:")
            
            user_states[user_id] = {"state": "waiting_contact_message"}
        return
    
    # Vip (admin)
    elif text == "⭐ Vip":
        if is_admin(user_id):
            data = load_data()
            vip_users = data.get("vip_users", [])
            
            vip_text = "⭐ VIP foydalanuvchilar:\n\n"
            if not vip_users:
                vip_text += "Hozircha VIP foydalanuvchilar yo'q\n"
            else:
                for i, vip_id in enumerate(vip_users, 1):
                    vip_text += f"{i}. ID: {vip_id}\n"
            
            vip_text += "\n📝 VIP qilish uchun foydalanuvchi ID yuboring\n📝 VIP dan o'chirish uchun ID ni qayta yuboring"
            
            await update.message.reply_text(vip_text)
            user_states[user_id] = {"state": "waiting_vip_user"}
        else:
            data = load_data()
            vip_message = data.get("vip_message")
            
            if vip_message:
                await update.message.reply_text(vip_message, reply_markup=user_menu())
            else:
                await update.message.reply_text("⭐ VIP haqida ma'lumot hali kiritilmagan", reply_markup=user_menu())
        return
    
    # ==================== USER TUGMALAR ====================
    
    # Anime qidirish
    elif text == "🔍 Anime qidirish":
        user_states[user_id] = {"state": "searching_anime"}
        await update.message.reply_text("🔍 Anime nomini kiriting:")
        return
    
    # Profil
    elif text == "👤 Profil":
        data = load_data()
        referral_count = len(data["referrals"].get(str(user_id), []))
        is_vip_user = user_id in data["vip_users"]
        
        bot = await context.bot.get_me()
        from utils import generate_referral_link
        ref_link = generate_referral_link(bot.username, user_id)
        
        profile_text = f"""👤 Profil

🆔 ID: {user_id}
⭐ Status: {'VIP' if is_vip_user else 'Oddiy'}
👥 Referal: {referral_count}/6

🎁 6 ta do'stni taklif qiling va 1 oy VIP oling!

🔗 Sizning referral havolangiz:
{ref_link}
"""
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        share_text = f"🎬 AniVoid botiga qo'shiling!\n\n{ref_link}"
        keyboard = [
            [InlineKeyboardButton("📤 Ulashish", url=f"https://t.me/share/url?url={ref_link}&text=" + share_text.replace('\n', '%0A'))]
        ]
        
        await update.message.reply_text(profile_text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    # Bog'lanish
    elif text == "📞 Bog'lanish":
        data = load_data()
        contact_message = data.get("contact_message")
        
        if contact_message:
            await update.message.reply_text(contact_message, reply_markup=user_menu())
        else:
            await update.message.reply_text("📞 Bog'lanish ma'lumotlari hali kiritilmagan", reply_markup=user_menu())
        return
    
    # ==================== MAXSUS TUGMALAR ====================
    
    # Tasdiqlash (yangi anime)
    elif text == "✅ Tasdiqlash":
        if user_id in user_states:
            state = user_states[user_id].get("state")
            
            if state == "waiting_episodes":
                # Yangi anime tasdiqlash
                from handlers.admin.anime_add import handle_confirm_episodes_keyboard
                await handle_confirm_episodes_keyboard(update, context)
                return
            
            elif state == "adding_episodes":
                # Qism qo'shish tasdiqlash
                from handlers.admin.ongoing import handle_confirm_new_episodes_keyboard
                await handle_confirm_new_episodes_keyboard(update, context)
                return
    
    # Bekor qilish
    elif text == "❌ Bekor qilish":
        if user_id in user_states:
            del user_states[user_id]
        await update.message.reply_text("❌ Bekor qilindi", reply_markup=admin_menu())
        return
    
    # Yuborish (kanalga)
    elif text == "✅ Yuborish":
        if user_id in user_states:
            state = user_states[user_id].get("state")
            
            if state == "anime_ready":
                from handlers.admin.anime_add import handle_send_new_anime_keyboard
                await handle_send_new_anime_keyboard(update, context)
                return
            
            elif state == "episodes_ready":
                from handlers.admin.ongoing import handle_send_to_channel_keyboard
                await handle_send_to_channel_keyboard(update, context)
                return
    
    # Orqaga
    elif text == "🔙 Orqaga":
        if is_admin(user_id):
            await update.message.reply_text("🔧 Boshqaruv paneli:", reply_markup=admin_menu())
        else:
            await update.message.reply_text("🏠 Asosiy menu:", reply_markup=user_menu())
        
        if user_id in user_states:
            del user_states[user_id]
        return
    
    # ==================== STATE HANDLERS ====================
    
    if user_id not in user_states:
        # Anime nomini tanlash (Ongoing dan)
        if text and text.startswith("☘️ "):
            await handle_anime_selected(update, context, text)
        return
    
    state_data = user_states[user_id]
    state = state_data.get("state")
    
    # Reklama xabari
    if state == "waiting_broadcast":
        await handle_broadcast_message(update, context)
        return
    
    # Anime nomi
    elif state == "waiting_anime_name":
        anime_name = update.message.text
        user_states[user_id] = {
            "state": "waiting_anime_post",
            "anime_name": anime_name,
            "is_hentai": state_data.get("is_hentai", False)
        }
        await update.message.reply_text(
            f"✅ Anime nomi: {anime_name}\n\n"
            f"📝 Endi kanal uchun post xabarini yuboring (rasm va matn):"
        )
    
    # Anime post
    elif state == "waiting_anime_post":
        try:
            msg = await context.bot.copy_message(
                chat_id=STORAGE_CHANNEL,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
            
            user_states[user_id]["post_message_id"] = msg.message_id
            user_states[user_id]["state"] = "waiting_episodes"
            user_states[user_id]["episodes"] = []
            
            # Tasdiqlash va Bekor qilish tugmalari
            keyboard = [
                [KeyboardButton("✅ Tasdiqlash"), KeyboardButton("❌ Bekor qilish")],
                [KeyboardButton("🔙 Orqaga")]
            ]
            
            await update.message.reply_text(
                "✅ Post saqlandi!\n\n"
                "📹 Endi qismlarni yuboring.\n"
                "Barcha qismlarni yuborganingizdan keyin '✅ Tasdiqlash' tugmasini bosing.",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Xato: {str(e)}\n\nBotni storage kanaliga admin qiling!",
                reply_markup=admin_menu()
            )
    
    # Yangi qismlar
    elif state in ["waiting_episodes", "adding_episodes"]:
        if update.message.video:
            anime_name = user_states[user_id].get("anime_name")
            
            if state == "adding_episodes":
                # Qism qo'shish
                current_count = user_states[user_id]["current_episode_count"]
                episode_num = current_count + len(user_states[user_id]["new_episodes"]) + 1
                
                try:
                    msg = await context.bot.copy_message(
                        chat_id=STORAGE_CHANNEL,
                        from_chat_id=update.effective_chat.id,
                        message_id=update.message.message_id,
                        caption=f"☘️ {anime_name}\n[{episode_num} - qism]"
                    )
                    
                    user_states[user_id]["new_episodes"].append(msg.message_id)
                except Exception as e:
                    await update.message.reply_text(f"❌ Xato: {str(e)}")
            else:
                # Yangi anime qo'shish
                episode_num = len(user_states[user_id]["episodes"]) + 1
                
                try:
                    msg = await context.bot.copy_message(
                        chat_id=STORAGE_CHANNEL,
                        from_chat_id=update.effective_chat.id,
                        message_id=update.message.message_id,
                        caption=f"☘️ {anime_name}\n[{episode_num} - qism]"
                    )
                    
                    user_states[user_id]["episodes"].append(msg.message_id)
                except Exception as e:
                    await update.message.reply_text(f"❌ Xato: {str(e)}")
    
    # Anime qidirish
    elif state == "searching_anime":
        anime_name = text
        data = load_data()
        
        found = None
        found_id = None
        for anime_id, anime_data in data["animes"].items():
            if anime_name.lower() in anime_data["name"].lower():
                found = anime_data
                found_id = anime_id
                break
        
        if found:
            try:
                from keyboards import watch_button
                await context.bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=STORAGE_CHANNEL,
                    message_id=found["post_id"],
                    reply_markup=watch_button(found_id)
                )
                await update.message.reply_text("✅ Anime topildi!", reply_markup=user_menu())
            except Exception as e:
                await update.message.reply_text(f"❌ Xato: {str(e)}", reply_markup=user_menu())
        else:
            await update.message.reply_text("❌ Anime topilmadi!", reply_markup=user_menu())
        
        del user_states[user_id]
    
    # VIP user
    elif state == "waiting_vip_user":
        try:
            vip_user_id = int(text.replace("-", ""))
            
            data = load_data()
            if vip_user_id in data["vip_users"]:
                data["vip_users"].remove(vip_user_id)
                await update.message.reply_text(f"✅ Foydalanuvchi {vip_user_id} VIP dan olib tashlandi", reply_markup=admin_menu())
            else:
                data["vip_users"].append(vip_user_id)
                await update.message.reply_text(f"✅ Foydalanuvchi {vip_user_id} VIP qilindi!", reply_markup=admin_menu())
            save_data(data)
            del user_states[user_id]
        except ValueError:
            await update.message.reply_text("❌ Noto'g'ri format! Faqat raqam kiriting!")
    
    # Admin action
    elif state == "waiting_admin_action":
        try:
            admin_id = int(text.replace("-", ""))
            data = load_data()
            
            if admin_id in data["admins"]:
                data["admins"].remove(admin_id)
                await update.message.reply_text(f"✅ {admin_id} adminlikdan olib tashlandi", reply_markup=admin_menu())
            else:
                data["admins"].append(admin_id)
                await update.message.reply_text(f"✅ {admin_id} admin qilindi!", reply_markup=admin_menu())
            save_data(data)
            del user_states[user_id]
        except ValueError:
            await update.message.reply_text("❌ Faqat raqam kiriting!")
    
    # Main channel
    elif state == "waiting_main_channel":
        try:
            channel_id = int(text.replace("-", ""))
            if channel_id > 0:
                channel_id = -channel_id
            
            data = load_data()
            
            if channel_id in data["main_channels"]:
                data["main_channels"].remove(channel_id)
                await update.message.reply_text(f"✅ Kanal olib tashlandi", reply_markup=admin_menu())
            else:
                data["main_channels"].append(channel_id)
                await update.message.reply_text(f"✅ Asosiy kanal qo'shildi!", reply_markup=admin_menu())
            save_data(data)
            del user_states[user_id]
        except ValueError:
            await update.message.reply_text("❌ Faqat raqam kiriting!")
    
    # Channel
    elif state == "waiting_channel":
        try:
            channel_id = int(text.replace("-", ""))
            if channel_id > 0:
                channel_id = -channel_id
            
            data = load_data()
            
            if channel_id in data["channels"]:
                data["channels"].remove(channel_id)
                await update.message.reply_text(f"✅ Kanal olib tashlandi", reply_markup=admin_menu())
            else:
                data["channels"].append(channel_id)
                await update.message.reply_text(f"✅ Kanal qo'shildi!", reply_markup=admin_menu())
            save_data(data)
            del user_states[user_id]
        except ValueError:
            await update.message.reply_text("❌ Faqat raqam kiriting!")
    
    # VIP message
    elif state == "waiting_vip_message":
        data = load_data()
        data["vip_message"] = text
        save_data(data)
        await update.message.reply_text("✅ VIP xabari saqlandi!", reply_markup=admin_menu())
        del user_states[user_id]
    
    # Contact message
    elif state == "waiting_contact_message":
        data = load_data()
        data["contact_message"] = text
        save_data(data)
        await update.message.reply_text("✅ Bog'lanish xabari saqlandi!", reply_markup=admin_menu())
        del user_states[user_id]
