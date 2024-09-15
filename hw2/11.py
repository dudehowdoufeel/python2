def get_chinese_zodiac(year):
    zodiac_signs = [
        "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]
    index = (year - 4) % 12
    return zodiac_signs[index]
year = int(input("Input your birth year: "))

zodiac_sign = get_chinese_zodiac(year)
print(f"Your Zodiac sign: {zodiac_sign}")
