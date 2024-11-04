def t(n):
    memo = {}

    def count_sequences(last_value, length):
        # If we have reached the desired length
        if length == n:
            return 1
        # Memoization check
        if (last_value, length) in memo:
            return memo[(last_value, length)]
        
        total_count = 0
        next_value = last_value + 1  # The next value must be greater than last_value

        # Iterate to find valid next values
        while True:
            # We need to check the bounded condition for all previous x_i
            valid = True
            for j in range(1, length + 1):
                # Check the condition x_i^j < (x_j + 1)^(x_i)
                if not (next_value ** j < (last_value + 1) ** next_value):
                    valid = False
                    break
            if valid:
                # Recur to the next value
                total_count += count_sequences(next_value, length + 1)
            next_value += 1  # Increment to try the next value
            
            # Condition to stop the loop based on the exponential growth
            if next_value ** (length + 1) >= (last_value + 1) ** next_value:
                break
            
        # Store the result in memoization
        memo[(last_value, length)] = total_count
        return total_count

    # Start counting sequences with the first element as 2
    return count_sequences(2, 1)

# Testing the function
print(f"t(2) = {t(2)}")  # Example: Should be 5
#print(f"t(10) = {t(10)}")  # Given: Should be 86195
#print(f"t(20) = {t(20)}")  # Given: Should be 5227991891
