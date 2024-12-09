from telegram.ext import Application,CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import tg_bot_navigation

# подгружаем переменные окружения
load_dotenv()

# передаем секретные данные в переменные
TOKEN = os.environ.get("TG_TOKEN")
# GPT_SECRET_KEY = os.environ.get("OPENAI_API_KEY")    

# передаем секретный токен chatgpt
# openai.api_key = GPT_SECRET_KEY


def main():
    application = Application.builder().token(TOKEN).concurrent_updates(True).build()
    print('Бот запущен...')

    start_handler = CommandHandler('start',tg_bot_navigation.start ,  block = False)
    application.add_handler(start_handler)

    # Регистрируем обработчик текстовых сообщений
    message_handler =MessageHandler(filters.TEXT & ~filters.COMMAND, tg_bot_navigation.handle_message,block = False)
    application.add_handler(message_handler)
    

    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()