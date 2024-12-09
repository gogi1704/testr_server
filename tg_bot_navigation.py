import aiohttp
from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup , KeyboardButton , ReplyKeyboardMarkup

async def handle_message(update, context )->int:
    text = update.message.text
    user_id = update.message.from_user.id
    print(context.user_data['state'])

    print(text)
    payload = {"text_answer":text,
               "user_id":user_id
               }
    if(text =="Начать заново"):
        await start(update, context)
    else:
    
        if (context.user_data['state'] == "terapevt"):     #terapevt
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(sock_connect=90, sock_read=120)) as session:
                async with session.post('http://127.0.0.1:5000/api/get_answer_terapevt', json=payload) as resp:    
                    text_json = await resp.json()
                    text = text_json['message']

                    is_terapevt_complete , new_text = await is_terapevt_result(text)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text = new_text)


                    if(is_terapevt_complete):
                        await terapevt_complete(update , context) 
                    
        elif(context.user_data['state'] == "manager"):                                               #manager
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(sock_connect=90, sock_read=120)) as session:
                async with session.post('http://127.0.0.1:5000/api/get_answer_manager', json=payload) as resp:         
                    text_json = await resp.json()
                    text = text_json['message']

                    if(text == "complete_manager"):
                        context.user_data['state'] = "terapevt"
                        await send_first_terapevt_message(update, context )
                    else:
                        await context.bot.send_message(chat_id=update.effective_chat.id, text = text)





async def start(update, context)->int:
    context.user_data['state'] = "manager"
    user_id = update.message.from_user.id

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(sock_connect=90, sock_read=120)) as session:
            payload = {"text_answer":"ok",
               "user_id":user_id
               }
            async with session.post('http://127.0.0.1:5000/api/start_new_dialog', json=payload) as resp:         
                text_json = await resp.json()
                text = text_json['message']

            if update.message:
                await update.message.reply_text(text)
            elif update.callback_query:
                await update.callback_query.message.reply_text(text)


async def terapevt_complete(update, context)->int:
    cancel_button = KeyboardButton("Начать заново")
    keyboard = [[cancel_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    text = "На это все. Можно начинать заново))"
    await update.message.reply_text(text , reply_markup=reply_markup)
    


async def send_first_terapevt_message(update, context)->int:
    await context.bot.send_message(chat_id=update.effective_chat.id, text = "Менеджер выяснил всю необходимую инофрмацию. Терапевт включается в беседу! (Это инфа для разработки)Ожидайте сообщение терапевта" )
    user_id = update.message.from_user.id
    payload = {"text_answer":"Ну что скажете",
               "user_id":user_id
               }
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(sock_connect=90, sock_read=120)) as session:
            async with session.post('http://127.0.0.1:5000/api/get_answer_terapevt', json=payload) as resp:         
                text_json = await resp.json()
                text = text_json['message']
                    
                await context.bot.send_message(chat_id=update.effective_chat.id, text = text)


async def is_terapevt_result(text):
    is_terapevt_result = False
    new_text = ""
    if "terapevt_result" in text:
        is_terapevt_result = True
        new_text = text.replace("terapevt_result", "")
    else:
        new_text = text
    print(f"Result = {is_terapevt_result} \n {new_text}")
    return is_terapevt_result, new_text