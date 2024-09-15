def get_astrological_sign(day, month):
    zodiac_signs = {
        'Aries': ((3, 21), (4, 19)),
        'Taurus': ((4, 20), (5, 20)),
        'Gemini': ((5, 21), (6, 20)),
        'Cancer': ((6, 21), (7, 22)),
        'Leo': ((7, 23), (8, 22)),
        'Virgo': ((8, 23), (9, 22)),
        'Libra': ((9, 23), (10, 22)),
        'Scorpio': ((10, 23), (11, 21)),
        'Sagittarius': ((11, 22), (12, 21)),
        'Capricorn': ((12, 22), (1, 19)),
        'Aquarius': ((1, 20), (2, 18)),
        'Pisces': ((2, 19), (3, 20))
    }
    
    for sign, (start, end) in zodiac_signs.items():
        start_month, start_day = start
        end_month, end_day = end
        
        if start_month == 12 and end_month == 1:
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                return sign
        else:
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                return sign
    
    return "Unknown Sign"

day = int(input("Input birthday: "))
month_name = input("Input month of birth (e.g. march, july etc): ").lower()

months = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5,
    'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10,
    'november': 11, 'december': 12
}

month = months.get(month_name)

if month:
    sign = get_astrological_sign(day, month)
    print(f"Your Astrological sign is: {sign}")
else:
    print("Invalid month name. Please enter a valid month.")
