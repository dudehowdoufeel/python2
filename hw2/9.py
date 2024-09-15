def get_season(month, day):
    if (month == 3 and day >= 20) or (month > 3 and month < 6) or (month == 6 and day <= 20):
        return "Spring"
    elif (month == 6 and day >= 21) or (month > 6 and month < 9) or (month == 9 and day <= 22):
        return "Summer"
    elif (month == 9 and day >= 23) or (month > 9 and month < 12) or (month == 12 and day <= 20):
        return "Autumn"
    elif (month == 12 and day >= 21) or (month < 3) or (month == 3 and day < 20):
        return "Winter"

def month_name(month):
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    return months[month - 1]

month = int(input("Input the month (e.g. [1-12]): "))
day = int(input("Input the day: "))
season = get_season(month, day)
month_name_str = month_name(month)

print(f"{month_name_str}, {day}. Season is {season}")
