def prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes_4k_plus_1(limit):
    primes = []
    k = 0
    while 4 * k + 1 < limit:
        if prime(4 * k + 1):
            primes.append(4 * k + 1)
        k += 1
    return primes

primes = get_primes_4k_plus_1(150)
print("primes of form 4k+1 less than 150:")
print(primes)
print()

def result(N):
    solutions = []
    for a in range(int(N ** 0.5) + 1):
        b_squared = N - a * a
        b = int(b_squared ** 0.5)
        if b * b == b_squared and a <= b:
            solutions.append((a, b))
    return solutions

def S(N):
    return sum(a for a, _ in result(N))

def main():
    while True:
        user_input = input("\nEnter N: ").strip()
        
        if user_input.lower() == 'q':
            break
        
        try:
            N = int(user_input)
            solutions = result(N)
            if solutions:
                print(f"For N = {N}:")
                solution_strings = []
                for a, b in solutions:
                    solution_strings.append(f"a = {a} b = {b}")
                print(" and ".join(solution_strings))
                s_value = S(N)
                print(f"S({N}) = {s_value}")
            else:
                print(f"no solutions found for {N}")
        except ValueError:
            print("please enter a valid integer")

if __name__ == "__main__":
    main()