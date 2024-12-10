from openai import OpenAI
from dotenv import load_dotenv
import openai
import os


load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()

system = """
Ты опытный терапевт.Ты работаешь в компании ООО ,,Человек,, Ты всегда ответственно подходишь к своей работе. 
Тебе будет передан список вопросов которые необходимо задать пациенту и саммаризированный диалог с пациентом.
Твоя задача - получить ответы на все вопросы из списка . Клиент не должен ничего знать о списке вопросов.
Вопросы пациенту необходимо задавать по одному.
"""



async def get_terapevt_answer(user_input , summary_dialog , terapevt_questions):
    user =f"""
Диалог с пациентом:
{summary_dialog}
Список вопросов:
{terapevt_questions}

1. Проанализируй диалог и выясни на какие вопросы из списка еще нет ответа в диалоге.(не упоминай список в ответе)
2. Задай вопрос из списка, на который еще нет ответа в диалоге.

ответ пациента : {user_input}
"""
    messages =[
                {"role": "system", "content": system},
                {"role": "user", "content": f"{user}" }
                ]
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )

    return completion.choices[0].message.content

