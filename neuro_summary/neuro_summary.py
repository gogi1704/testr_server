from openai import OpenAI
# from dotenv import load_dotenv
import openai
import os

# load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')


system = """
Ты - нейро-саммаризатор. Твоя задача - саммаризировать диалог, который тебе пришел. 
Ты должен избавится от воды в диалоге и оставить только самое важное.
Если в диалоге есть личные данные , такие как имя , возраст, вес, моб телефон или подобное
обязательно сохрани их в саммаризации.
"""

client = OpenAI()

async def summarize_dialog(dialog):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": """Саммаризируй следующий диалог менеджера и клиента, 
         тебе запрещено удалять из саммаризации все данные клиента. Вот диалог: """ + dialog}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",     # используем gpt4 для более точной саммаризации
        messages=messages,
        temperature=0,          # Используем более низкую температуру для более определенной суммаризации
    )

    return completion.choices[0].message.content

