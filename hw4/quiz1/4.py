def five(a, b):
    with open(a, 'r') as infile, open(b, 'w') as outfile:
        for line in infile:
            username, score = line.split()
            new_score = int(score) + 5
            outfile.write(f"{username} {new_score}\n")

a = r'C:\Users\ASUS\Desktop\python2\hw4\quiz1\class_scores.txt'
b = 'scores2.txt'

five(a, b)

print("donie")
