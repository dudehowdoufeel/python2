file_path = r'C:\Users\ASUS\Desktop\python2\hw3\grades1.txt'

def grades(file_path):
    passed = 0

    with open(file_path, 'r') as file:
        for line in file:
            name, scores_str = line.split(maxsplit=1)
            scores = eval(scores_str.strip())
            if all(score >= 50 for score in scores):
                passed += 1

    return passed

result = grades(file_path)
print(f"passed all three tests: {result}")
