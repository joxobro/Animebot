import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters
from config import TOKEN
from handlers.start import start_command
from handlers.callback_handler import handle_callback
from handlers.message_handler import handle_message
from handlers.watch_anime import handle_watch_anime
from handlers.inline_search import handle_inline_query

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Start command
    async def start_wrapper(update, context):
        if context.args and (context.args[0].startswith('watch_') or context.args[0].startswith('watchh_')):
            await handle_watch_anime(update, context)
        else:
            await start_command(update, context)
    
    application.add_handler(CommandHandler("start", start_wrapper))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.ALL, handle_message))
    application.add_handler(InlineQueryHandler(handle_inline_query))
    
    print("🤖 AniVoid bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
