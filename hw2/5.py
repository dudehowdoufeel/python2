def get_days_in_month(month_name):
    months = {
        'January': 31,
        'February': '28/29',
        'March': 31,
        'April': 30,
        'May': 31,
        'June': 30,
        'July': 31,
        'August': 31,
        'September': 30,
        'October': 31,
        'November': 30,
        'December': 31
    }

    if month_name not in months:
        return "Invalid month name. Please enter a valid month name."
    
    return months[month_name]

month_name = input("Input the name of the Month: ")
days = get_days_in_month(month_name)
print(f"No. of days: {days}")
