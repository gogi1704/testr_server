from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import main
import db.user_history_db as sql_db
import baza.doctors_baza as doctors_baza
import os


input = input("Введите ваш openai key: ")
os.environ["OPENAI_API_KEY"] = input

# создаем объект приложения
app = FastAPI()
sql_db.init_db()
doctors_baza.load_doctors_baza()
# настройки для работы запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class AnswerRequest(BaseModel):
    text_answer:str
    user_id: int

@app.post("/api/get_answer_manager")
async def get_answer_manager(request: AnswerRequest):
    try:
        text = await main.run_dialog_manager(request.text_answer , request.user_id)
        return {"message": text}
    
    except Exception as e:
         return {"message": "Error "+ str(e)}
    
@app.post("/api/get_answer_terapevt")
async def get_answer_terapevt(request: AnswerRequest):
    try:
        text = await main.run_dialog_terapevt(request.text_answer , request.user_id)
        return {"message": text}
    
    except Exception as e:
         return {"message": "Error "+ str(e)}
    


@app.post("/api/start_new_dialog")
async def start_new_dialog(request: AnswerRequest):
    try:
        text = await main.start_new_dialog(request.user_id)
        return {"message": text}
    
    except Exception as e:
         return {"message": "Error "+ str(e)}
    


@app.post("/api/complete_dialog")
async def complete_dialog(request: AnswerRequest):
    try:
        text = await main.start_new_dialog(request.user_id)
        return {"message": text}
    
    except Exception as e:
         return {"message": "Error "+ str(e)}