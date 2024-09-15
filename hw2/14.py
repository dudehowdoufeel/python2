def calculate_sum_and_average():
    numbers = []
    
    while True:
        input_str = input("Enter integers (0 to finish, space-separated): ")
        input_list = input_str.split()
        
        for item in input_list:
            try:
                num = int(item)
                if num == 0:
                    if numbers:
                        total_sum = sum(numbers)
                        average = total_sum / len(numbers)
                        print(f"The sum is {total_sum}.")
                        print(f"The average is {average:.2f}.")
                    else:
                        print("No numbers were entered.")
                    return
                numbers.append(num)
            except ValueError:
                print("Please enter valid integers.")
calculate_sum_and_average()
