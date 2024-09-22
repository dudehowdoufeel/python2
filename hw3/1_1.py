import random
names = ["almas", "abdu", "maiki", "kesha", "chara","miya", "bekzat", "islam", "amir", "olzhas","ilyas", "gulken", "inkar", "sanzhar", "asem"]

def randomScore():
    return [random.randint(0, 100) for _ in range(3)]

for name in names:
    scores = randomScore()
    print(name, scores)
