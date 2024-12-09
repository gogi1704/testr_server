from openai import OpenAI
# from dotenv import load_dotenv
import openai
import os


# load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI()

system = """
Ты опытный терапевт.Ты работаешь в компании ООО ,,Человек,, Ты всегда ответственно подходишь к своей работе. 
Твоя задача - выявить жалобы пациента из полученного диалога и составить 2-3 вопросов 
которые помогут более точно понять проблему пациента и определить к какому специалисту необходимо направить пациента.
Ты не должен задавать вопросы, которые не относятся к теме беседы.
"""



async def get_terapevt_questions(summary_dialog):
    user =f"""
Необходимо действовать согласно инструкциям.
В твоем распоряжении будет саммаризированный диалог с пациентом.

Диалог с пациентом:
{summary_dialog}
Делай все по порядку.
1. Проанализируй диалог и выясни что беспокоит пациента.
2 .Составь вопросы которые тебе необходимо задать пациенту (максимум 2-3 вопросов) , чтобы наиболее точно понять проблему пациента.
в ответе пришли пронумерованный список вопросов.

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

