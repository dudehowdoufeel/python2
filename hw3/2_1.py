import random

names = ["almas", "abdu", "maiki", "kesha", "chara","miya", "bekzat", "islam", "amir", "olzhas","ilyas", "gulken", "inkar", "sanzhar", "asem"]

def random_time():
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    return f"{hours:02}:{minutes:02}" 

for name in names:
    entry_hour = random.randint(0, 23)
    entry_minute = random.randint(0, 59)
    
    entry_time = f"{entry_hour:02}:{entry_minute:02}"

    exit_hour = entry_hour
    exit_minute = entry_minute
    
    while True:
        exit_hour = random.randint(entry_hour, 23)
        exit_minute = random.randint(0, 59)
        if exit_hour > entry_hour or (exit_hour == entry_hour and exit_minute > entry_minute):
            break

    exit_time = f"{exit_hour:02}:{exit_minute:02}"
    print(f"{name} {entry_time}, {exit_time}")
