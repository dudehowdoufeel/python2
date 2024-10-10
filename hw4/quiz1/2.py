<<<<<<< HEAD
def unique_number(numbers):
    count_dict = {}
    
    for num in numbers:
        if num in count_dict:
            count_dict[num] += 1
        else:
            count_dict[num] = 1

    for num, count in count_dict.items():
        if count == 1:
            return num

a = input("enter a list of numbers separated by commas: ")
a_list = [float(num.strip()) for num in a.split(",")]

result = unique_number(a_list)
print(result)
