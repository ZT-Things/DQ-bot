import sqlite3
from settings import *

def get_days_diff():
    current_date = datetime.now()
    days_difference =  (current_date - START_DATE).days + 1
    return days_difference

def get_question(index, range=1):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if not index:
        print("Specify index")
        return None

    cursor.execute("SELECT * FROM Questions WHERE Counter >= ? ORDER BY Counter ASC LIMIT ?", (index, range))

    results = cursor.fetchall()

    conn.close()

    return results

def get_question_amount():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Questions")
    count = cursor.fetchone()[0]

    conn.close()

    return int(count)

def add_dq(title: str, choices: str, suggested=False, owner="SmolBooster", index=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    counter = get_question_amount() + 1

    if index:
        counter = int(index)
        cursor.execute("UPDATE Questions SET counter = counter + 1 WHERE counter >= ?", (index,))

    cursor.execute("INSERT INTO Questions (question_text, choices_text, counter, suggested, owner) VALUES (?, ?, ?, ?, ?)", (title, choices, counter, suggested, owner))
        

    conn.commit()
    conn.close()
    
def pop_dq():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    counter = get_question_amount()

    cursor.execute("DELETE FROM Questions WHERE counter = ?", (counter,))

    conn.commit()
    conn.close()

if __name__ == "__main__":

    x = get_question(1)
    print(x)

    pass