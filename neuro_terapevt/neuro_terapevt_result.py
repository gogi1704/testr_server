from openai import OpenAI
from dotenv import load_dotenv
import openai
import os
import re


load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()

system_result = """
Ты лучший терапевт и ты отлично ориентируешься в диагнозах и медицинский рекомендациях. 
Тебе будет передан диалог с пациентом.
Твоя задача проанализировать диалог и выяснить как помочь пациенту.
"""

system_recomendation = """
Ты специалист отдела кадров в медицинской компании. Ты знаешь все о наших сотрудниках.
Тебе будут переданы документы с информацией о сотрудниках и рекомендации терапевта. Клиент не должен знать о переданных документах.
Твоя задача проанализировать документы , рекомендации терапевта и предоставить информацию о сотруднике.
"""



async def get_terapevt_result_answer(summary_dialog):
    user =f"""

Саммаризированный Диалог с клиентом:
{summary_dialog}

Ответ пришли в формате -
terapevt_result
Рекомендации терапевта: ...
Обратиться к специалисту: ...(только специализация врача , например : Лор,хирург и т.д.)
"""
    messages =[
                {"role": "system", "content": system_result},
                {"role": "user", "content": f"{user}" }
                ]
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )


    print(f"Manager questions cheker answer: {completion.choices[0].message.content}")
    return completion.choices[0].message.content 



async def get_recomendation_doc(chunks,terapevt_result):
    message_content = re.sub(r'\n{2}', ' ', '\n '.join([f'\nОтрывок документа №{i+1}\n=====================' + doc.page_content + '\n' for i, doc in enumerate(chunks)]))
    
    user =f"""
    Сформируй ответ в формате:

    terapevt_result
    Рекомендуем обратиться к спнциалисту : Имя специалиста.
    Образование специалиста: ...
    Специализация: ...
    Контакты специалиста: ...

"""
    messages =[
                {"role": "system", "content": system_recomendation},
                {"role": "user", "content": f"{user} . Вот документы о сотрудниках: {message_content} . Рекомендации терапевта: {terapevt_result}" }
                ]
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )


    print(f"Manager questions cheker answer: {completion.choices[0].message.content}")
    return completion.choices[0].message.content 
