from datetime import datetime, timedelta

def get_next_day(year, month, day):
    current_date = datetime(year, month, day)
    next_day = current_date + timedelta(days=1)
    return next_day.strftime("%Y-%m-%d")

year = int(input("Input a year: "))
month = int(input("Input a month [1-12]: "))
day = int(input("Input a day [1-31]: "))
next_date = get_next_day(year, month, day)
print(f"The next date is {next_date}.")
