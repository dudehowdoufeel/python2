def vowelOrNot(letter):
    vowels = 'aeiouAEIOU'
    if letter.isalpha() and len(letter) == 1:
        if letter in vowels:
            return f"{letter} is a vowel."
        else:
            return f"{letter} is a consonant."
    else:
        return "Invalid input. Please enter a single alphabetic letter."
letter = input("Input a letter of the alphabet: ")
result = vowelOrNot(letter)
print(result)
