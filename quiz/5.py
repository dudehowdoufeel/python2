def check_letters(word1, word2):
    return all(letter in word2 for letter in word1)

# Ввод слов
word1 = input("Введите первое слово: ")
word2 = input("Введите второе слово: ")

# Проверка и вывод результата
if check_letters(word1, word2):
    print("True")
else:
    print("False")
