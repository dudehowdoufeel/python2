from datetime import datetime

file_path = r'C:\Users\ASUS\Desktop\python2\hw3\logfile.txt'

def time_difference(entry, exit):
    format_str = "%H:%M"
    vxod = datetime.strptime(entry.strip(), format_str)
    vyxod = datetime.strptime(exit.strip(), format_str)
    
    difference = (vxod - vyxod).total_seconds() / 60
    return difference

def chechie(file_path):
    online = []
    
    with open(file_path, 'r') as file:
        for line in file:
            name, times = line.split(maxsplit=1)
            entry, exit = times.split(', ')
       
            if time_difference(entry, exit) >= 60:
                online.append(name)
    
    return online

users = chechie(file_path)
print("users who were online for at least an hour:", users)
