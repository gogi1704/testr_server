from openai import OpenAI
# from dotenv import load_dotenv
import openai
import os


# load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()

system = """
Ты лучший копирайтер и ты отлично ориентируешься в тексте. 
Тебе будет передан список вопросов и  диалог с клиентом.
Твоя задача проверить есть ли в диалоге вся информация о клиенте .
Все вопросы из списка обязательно должны быть заданы клиенту.
"""



async def get_manager_questions_cheker_answer(summary_dialog , questions):
    user =f"""

Диалог с клиентом:
{summary_dialog}
Вопросы :
{questions}
Если в диалоге есть все вопросы и ответы на них в переданном тебе документе то пришли : complete_terapevt. 
Если в диалоге нет всей необходимой информации то пришли : incomplete_terapevt.
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


    print(f"Terapevt questions cheker answer: {completion.choices[0].message.content}")
    return completion.choices[0].message.content 

