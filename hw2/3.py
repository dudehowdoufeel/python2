def doggie(human):
    if human_years <= 2:
        dog_years = human_years * 10.5
    else:
        dog_years = 2 * 10.5 + (human_years - 2) * 4
    return dog_years

human_years = float(input("Input a dog's age in human years: "))
dog_years = doggie(human_years)
print(f"The dog's age in dog's years is {dog_years}")
