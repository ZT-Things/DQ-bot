import sqlite3
from settings import *

def get_days_diff():
    current_date = datetime.now()
    days_difference =  (current_date - START_DATE).days + 1
    return days_difference

def get_current_question():
    pass

def get_question_amount():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Questions")
    count = cursor.fetchone()[0]

    conn.close()

    return int(count)

def add_daily_question(title: str, choices: str, suggested=False, owner="SmolBooster"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    counter = get_question_amount() + 1

    cursor.execute("INSERT INTO Questions (question_text, choices_text, counter, suggested, owner) VALUES (?, ?, ?, ?, ?)", (title, choices, counter, suggested, owner))

    conn.commit()
    conn.close()
    
