def translator(word):
    vowels = 'aeiou'
    
    if word[0].lower() in vowels:
        return word + 'yay'
    
    for i, letter in enumerate(word):
        if letter.lower() in vowels:
            return word[i:] + word[:i] + 'ay'
    return word

def translate_sentence(a):
    return ' '.join(translator(word) for word in a.split())

a = input()
print(translate_sentence(a))
