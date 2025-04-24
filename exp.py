from datetime import datetime
from settings import START_DATE

current_date = datetime.now()

date_difference = (current_date - START_DATE).days + 1

print(date_difference)