import sqlite3

def init_db():
    connection = sqlite3.connect('users_history.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS messages
                   (user_id INTEGER , message TEXT) 
                   """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS terapevt_questions
                   (user_id INTEGER , questions TEXT) 
                   """)
    connection.commit()
    connection.close()


def add_questions(user_id, questions):
    connection = sqlite3.connect('users_history.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO terapevt_questions (user_id, questions) VALUES (?, ?)", (user_id, questions))
    connection.commit()
    connection.close()

def get_questions(user_id):
    connection = sqlite3.connect('users_history.db')
    cursor = connection.cursor()
    cursor.execute("SELECT questions FROM terapevt_questions WHERE user_id = ?", (user_id,))
    questions = cursor.fetchone()
    connection.close()
    return questions[0] if questions else None
    

def add_or_update_message(user_id, message):
    connection = sqlite3.connect('users_history.db')
    cursor = connection.cursor()
    
    # Проверяем, существует ли запись с данным user_id
    cursor.execute("SELECT * FROM messages WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        # Если запись существует, обновляем её
        cursor.execute("UPDATE messages SET message = ? WHERE user_id = ?", (message, user_id))
    else:
        # Если записи нет, добавляем новую
        cursor.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", (user_id, message))
    
    connection.commit()
    connection.close()

def get_history_by_id(user_id):
    connection = sqlite3.connect('users_history.db')
    cursor = connection.cursor()
    cursor.execute("SELECT message FROM messages WHERE user_id = ?", (user_id,))
    messages = cursor.fetchall()
    connection.close()
    # Преобразуем список кортежей в список строк
    return [message[0] for message in messages]

def remove_history_by_id(user_id):
    connection = sqlite3.connect('users_history.db')
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM messages WHERE user_id = ?""", (user_id,))
    connection.commit()
    connection.close()

def remove_questions_by_id(user_id):
    connection = sqlite3.connect('users_history.db')
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM terapevt_questions WHERE user_id = ?""", (user_id,))
    connection.commit()
    connection.close()

