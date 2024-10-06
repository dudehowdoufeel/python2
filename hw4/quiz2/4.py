def update(a, b):
    with open(a, 'r') as infile, open(b, 'w') as outfile:
        for line in infile:
            parts = line.split()
            if len(parts) == 4:  
                surname, name, email, phone = parts
                surname = surname.capitalize()
                name = name.capitalize()
                phone = '301 ' + phone
                outfile.write(f"{surname} {name} {email} {phone}\n")

a=r'C:\Users\ASUS\Desktop\python2\hw4\quiz2\student.txt'
b = 'student2.txt'


update(a, b)
