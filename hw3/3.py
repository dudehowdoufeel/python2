import re
file_path = r'C:\Users\ASUS\Desktop\python2\hw3\wordlist.txt'

ime_words = []
with open(file_path, 'r') as file:
    for line in file:
        word = line.strip() 
        if word.endswith('ime'):
            ime_words.append(word)

ave_words = []
with open(file_path, 'r') as file:
    for line in file:
        word = line.strip()  
        if len(word) >= 4 and word[1:4] == 'ave':
            ave_words.append(word)

total_words = 0
count_letters = 0
count_r_s_t_l_n = 0

letters_to_check = set('rstln')
letters_to_count = set('rstlne')

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        words = line.split()
        total_words += len(words)
        
        for word in words:
            if letters_to_count.intersection(word):
                count_letters += 1
            if letters_to_check.intersection(word):
                count_r_s_t_l_n += 1

percen= (count_r_s_t_l_n / total_words) * 100 if total_words > 0 else 0


no_vowel_words = []
vowels = set('aeiou')

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        words = line.split()  
        for word in words:
            cleaned_word = re.sub(r'[^a-zA-Z]', '', word) 
            if cleaned_word and not vowels.intersection(cleaned_word.lower()):
                no_vowel_words.append(cleaned_word)



words_with_all_vowels = []

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        words = line.split() 
        for word in words:
            cleaned_word = re.sub(r'[^a-zA-Z]', '', word) 
            if cleaned_word and vowels.issubset(set(cleaned_word.lower())): 
                words_with_all_vowels.append(cleaned_word)

#results
if ime_words:
    print("Words ending with 'ime':", ", ".join(ime_words))
else:
    print("no such words")

if ave_words:
    print("All words whose second, third, and fourth letters are 'ave':",", ".join(ave_words))
else:
    print("no such words")

print(f'Total words: {total_words}')
print(f'Words containing at least one of r, s, t, l, n, e: {count_letters}')
print(f'Percentage of words containing at least one of r, s, t, l, n: {percen:.2f}%')


if no_vowel_words:
    print("Words with no vowels:")
    print(", ".join(no_vowel_words))
else:
    print("no such words")

if words_with_all_vowels:
    print("Words containing all vowels:")
    print(", ".join(words_with_all_vowels))
else:
    print("no such words")
