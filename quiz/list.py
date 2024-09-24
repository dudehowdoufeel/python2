def remove_duplicates(elements):
    return list(set(elements))

input_list = ['a', 'a', 'e', 'o', 'p', 'i', 'e', 'j']
unique_list = remove_duplicates(input_list)
print(f"Список без дубликатов: {unique_list}")
