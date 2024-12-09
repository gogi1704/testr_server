from openai import OpenAI
# from dotenv import load_dotenv
import openai
import os


# load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()

system = """
Ты менеджер медицинской компании ООО ,,Человек,,.Ты всегда ответственно подходишь к своей работе. 
Твоя задача - выявить информацию о клиенте в диалоге.Тебе будет передан спиcок вопросов которые необходимо выяснить у клиента 
и уже имеющийся диалог с клиентом.
Не нужно нумеровать вопросы в своем ответе.
Не надо приветствовать клиента. Вопросы пациенту необходимо задавать по одному в порядке  их следования в списке.
Вопросы не должны повторяться.
"""



async def get_manager_answer(user_input , summary_dialog):
    user =f"""
Диалог с клиентом:
{summary_dialog}
Список вопросов:
1. Имя клиента.
2. возраст клиента.
3. проходил ли мед осмотр в нашей компании, если да то на каком предприятии(компания,учебное учереждение ....) это происходило.
4. Какие у клиента проблемы или жалобы.(обязательный вопрос)


Вот вопрос или ответ клиента : {user_input}
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

