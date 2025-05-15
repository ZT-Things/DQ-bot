import sqlite3
from settings import *
from datetime import datetime, timedelta, time

def get_days_diff():
    current_date = datetime.now()
    current_time = current_date.time()

    # Check if the current time is before 17:00
    if current_time < time(17, 0):
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    else:
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)

    days_difference = (current_date - START_DATE).days + 1
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

def remove_dq(counter):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Questions WHERE counter = ?", (counter,))
    cursor.execute("UPDATE Questions SET counter = counter - 1 WHERE counter > ?", (counter,))

    conn.commit()
    conn.close()

def get_choices(info):

    return info[2].split("%")

def parse_dq(info, votes=None):
    id = info[0]
    title = info[1]
    choices = info[2].split("%")
    date = info[3]
    counter = info[4]
    suggested = True if info[5] == 1 else False
    host = info[6]

    dq = f"""**[{counter}] Daily question — """

    if suggested:
        dq += f"Suggested by {host}"
    else:
        dq += f"Hosted by {host}"

    dq += f"""**\nQ: {title}?\n"""

    c = 1


    if not votes:
        for i in choices:
            dq += f"\n{c}: {i} (0 votes)"
            c += 1
    else:
        for i in range(len(choices)):
            dq += f"\n{c}: {choices[i]} ({int(votes[i]) - 1} votes)"
            c += 1

    return dq

if __name__ == "__main__":

    x = get_question(1, 2)
    print(x)

    pass