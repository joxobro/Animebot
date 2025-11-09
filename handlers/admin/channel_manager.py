from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data, save_data
from keyboards import admin_menu
import re

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, is_main: bool = False):
    """Kanal qo'shish - ID, username yoki link"""
    user_id = update.effective_user.id
    data = load_data()
    
    channel_key = "main_channels" if is_main else "channels"
    
    # 1. ID orqali (-100...)
    if text.startswith('-') or text.isdigit():
        try:
            channel_id = int(text)
            if channel_id > 0:
                channel_id = -channel_id
            
            # Tekshirish
            try:
                chat = await context.bot.get_chat(channel_id)
                
                if channel_id in data[channel_key]:
                    data[channel_key].remove(channel_id)
                    await update.message.reply_text(f"✅ Kanal olib tashlandi: {chat.title}", reply_markup=admin_menu())
                else:
                    data[channel_key].append(channel_id)
                    await update.message.reply_text(f"✅ Kanal qo'shildi: {chat.title}", reply_markup=admin_menu())
                
                save_data(data)
            except Exception as e:
                await update.message.reply_text(f"❌ Kanal topilmadi yoki bot admin emas!\n\nXato: {str(e)}", reply_markup=admin_menu())
                
        except ValueError:
            await update.message.reply_text("❌ Noto'g'ri format!", reply_markup=admin_menu())
    
    # 2. Username orqali (@channel)
    elif text.startswith('@'):
        username = text[1:]
        try:
            chat = await context.bot.get_chat(f"@{username}")
            channel_id = chat.id
            
            if channel_id in data[channel_key]:
                data[channel_key].remove(channel_id)
                await update.message.reply_text(f"✅ Kanal olib tashlandi: {chat.title}", reply_markup=admin_menu())
            else:
                data[channel_key].append(channel_id)
                await update.message.reply_text(f"✅ Kanal qo'shildi: {chat.title}", reply_markup=admin_menu())
            
            save_data(data)
        except Exception as e:
            await update.message.reply_text(f"❌ Kanal topilmadi!\n\nXato: {str(e)}", reply_markup=admin_menu())
    
    # 3. Link orqali (https://t.me/joinchat/... yoki https://instagram.com/...)
    elif text.startswith('http'):
        # Telegram invite link
        if 'joinchat' in text or 't.me/+' in text:
            # Invite link ni ID ga aylantirish mumkin emas, shuning uchun to'g'ridan link saqlaymiz
            invite_code = text.split('/')[-1]
            
            # Link sifatida saqlash
            link_data = {
                "type": "invite_link",
                "url": text,
                "code": invite_code
            }
            
            # Link mavjudligini tekshirish
            links = data.get("channel_links", [])
            
            found = None
            for i, link in enumerate(links):
                if link.get("url") == text:
                    found = i
                    break
            
            if found is not None:
                links.pop(found)
                data["channel_links"] = links
                await update.message.reply_text("✅ Link olib tashlandi", reply_markup=admin_menu())
            else:
                links.append(link_data)
                data["channel_links"] = links
                await update.message.reply_text("✅ Telegram invite link qo'shildi", reply_markup=admin_menu())
            
            save_data(data)
        
        # Boshqa ijtimoiy tarmoq linklari (Instagram, YouTube, etc.)
        else:
            link_data = {
                "type": "external_link",
                "url": text
            }
            
            links = data.get("external_links", [])
            
            found = None
            for i, link in enumerate(links):
                if link.get("url") == text:
                    found = i
                    break
            
            if found is not None:
                links.pop(found)
                data["external_links"] = links
                await update.message.reply_text("✅ Link olib tashlandi", reply_markup=admin_menu())
            else:
                links.append(link_data)
                data["external_links"] = links
                await update.message.reply_text("✅ Tashqi link qo'shildi\n\n⚠️ Eslatma: Tashqi linklar majburiy obunada tekshirilmaydi, faqat ko'rsatiladi.", reply_markup=admin_menu())
            
            save_data(data)
    
    else:
        await update.message.reply_text(
            "❌ Noto'g'ri format!\n\n"
            "Quyidagi formatlardan foydalaning:\n"
            "• Kanal ID: -1001234567890\n"
            "• Username: @channel\n"
            "• Telegram link: https://t.me/+xxxxx\n"
            "• Boshqa link: https://instagram.com/...",
            reply_markup=admin_menu()
        )

async def show_channels(update: Update, context: ContextTypes.DEFAULT_TYPE, is_main: bool = False):
    """Kanallarni ko'rsatish"""
    data = load_data()
    
    channel_key = "main_channels" if is_main else "channels"
    channels = data.get(channel_key, [])
    channel_links = data.get("channel_links", [])
    external_links = data.get("external_links", [])
    
    text = "✅ Asosiy kanallar:\n\n" if is_main else "📱 Majburiy obuna kanallari:\n\n"
    
    if not channels and not channel_links and not external_links:
        text += "Hozircha kanallar yo'q\n"
    else:
        # Oddiy kanallar
        for i, ch_id in enumerate(channels, 1):
            try:
                chat = await context.bot.get_chat(ch_id)
                text += f"{i}. {chat.title}\n   ID: {ch_id}\n\n"
            except:
                text += f"{i}. ID: {ch_id} (Noma'lum)\n\n"
        
        # Invite linklar
        for i, link in enumerate(channel_links, len(channels) + 1):
            text += f"{i}. 🔗 Telegram invite link\n   {link['url']}\n\n"
        
        # Tashqi linklar
        for i, link in enumerate(external_links, len(channels) + len(channel_links) + 1):
            text += f"{i}. 🌐 Tashqi link\n   {link['url']}\n\n"
    
    text += "\n📝 Kanal qo'shish:\n"
    text += "• ID: -1001234567890\n"
    text += "• Username: @channel\n"
    text += "• Telegram link: https://t.me/+xxxxx\n"
    text += "• Boshqa link: https://instagram.com/...\n\n"
    text += "📝 O'chirish uchun qayta yuboring"
    
    await update.message.reply_text(text)
