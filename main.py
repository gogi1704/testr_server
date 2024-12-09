
import neuro_summary.neuro_summary as summary
import neuro_manager.neuro_manager as manager
import neuro_manager.neuro_manager_questions_cheker as manager_que_cheker
import neuro_terapevt.neuro_terapevt_questions_cheker as terapevt_que_cheker
import neuro_terapevt.neuro_terapevt as terapevt
import neuro_terapevt.neuro_terapevt_result as terapevt_result
import neuro_terapevt.neuro_terapevt_questions as terapevt_questions
import db.user_history_db as db
import baza.doctors_baza as docators_baza

import time




async def chat_with_manager(user_say, summarized_history , user_id): 
    manager_say = await manager.get_manager_answer(user_say, summarized_history)

    manager_say_text = f"Менеджер задает вопрос: {manager_say} "   
    history = db.get_history_by_id(user_id)
    history.append(manager_say_text)
    
    db.add_or_update_message(user_id=user_id , message= ''.join(history))

    return manager_say


async def chat_with_terapevt(user_say, summarized_history , user_id , terapevt_questions): 

    terapevt_say = await terapevt.get_terapevt_answer(user_say, summarized_history , terapevt_questions)

    terapevt_say_text = f"Терапевт : {terapevt_say} "

    history = db.get_history_by_id(user_id)
    history.append(terapevt_say_text)
    
    db.add_or_update_message(user_id=user_id , message= ''.join(history))

    return terapevt_say

async def make_terapevt_questions(user_id):
    summarized_history = await get_dialog_from_db(user_id)
    questions = await terapevt_questions.get_terapevt_questions(summary_dialog= summarized_history)
    print(f"Terapevt questions: {questions}" )
    db.add_questions(user_id=user_id , questions=questions)


async def run_dialog_manager(user_say , user_id):
    history_dialog_from_db = await get_dialog_from_db(user_id)
    history_dialog = f"{history_dialog_from_db} Клиент отвечает:{user_say}"
    db.add_or_update_message(user_id=user_id , message=history_dialog)

    print(f"in runDialog_manager{history_dialog}")

    is_manager_complete = await manager_que_cheker.get_manager_questions_cheker_answer(summary_dialog= history_dialog)
    if(is_manager_complete == "complete_manager"):
        sum_history = await summary.summarize_dialog(history_dialog)
        db.add_or_update_message(user_id=user_id , message=sum_history)
        
        return is_manager_complete
    else:
        manager_say = await chat_with_manager(user_say = user_say,summarized_history = history_dialog , user_id= user_id)
        return manager_say
    


async def run_dialog_terapevt(user_say , user_id):
    terapevt_questions = db.get_questions(user_id)

    if (terapevt_questions == None):
        await make_terapevt_questions(user_id)
        history = db.get_history_by_id(user_id)
        history.append("Терапевт выяснил всю необходимую информацию и дал рекомендации.")   
        db.add_or_update_message(user_id=user_id , message= ''.join(history)) 
        terapevt_questions = db.get_questions(user_id)
    
    history_dialog_from_db = await get_dialog_from_db(user_id)
    history_dialog = f"{history_dialog_from_db} Пациент отвечает:{user_say}"
    db.add_or_update_message(user_id=user_id , message=history_dialog)

    # print(f"in runDialog_terapevt{history_dialog}")

    is_terapevt_complete = await terapevt_que_cheker.get_manager_questions_cheker_answer(summary_dialog= history_dialog , questions= terapevt_questions )
    print(is_terapevt_complete)

    if(is_terapevt_complete == "complete_terapevt"):
        terapevt_say = await terapevt_result.get_terapevt_result_answer(history_dialog)
        sum_history = await summary.summarize_dialog(history_dialog)
        db.add_or_update_message(user_id=user_id , message=sum_history)

        
        chunks = await docators_baza.get_chunks("doctors_baza.txt" , terapevt_say , 2)
        recomendations = await terapevt_result.get_recomendation_doc(chunks= chunks, terapevt_result=terapevt_say)
        #
        print(recomendations)
        return recomendations
    else:
        terapevt_say = await chat_with_terapevt(user_say = user_say,summarized_history = history_dialog , user_id= user_id , terapevt_questions = terapevt_questions)
        return terapevt_say




async def get_dialog_from_db(user_id):

    history = db.get_history_by_id(user_id)
    if len(history) > 0:
        # summarized_history = await summary.summarize_dialog("".join(history))
        history_text = "".join(history)
    else :
        history_text = ""
    
    return history_text


async def start_new_dialog(user_id):
    db.remove_history_by_id(user_id)
    db.remove_questions_by_id(user_id)

    text = "Привет, я менеджер компании <<Человек>>. Как я могу к вам обращаться?"
    print(f"Start_dialog_fun")
    db.add_or_update_message(user_id=user_id , message=text)
    return text




