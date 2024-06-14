import random

FOURLETTERNAMESPATH = "four_letter_names.txt"

def generateOppositeSameQuestions(level: int=3, names: list=None):
    if names is None:
        names = get_four_letter_names()
    chosens = random.sample(names, level)
    while True:
        group_a, group_b = separate_into_groups(chosens)
        if len(group_a) == 0 or len(group_b) == 0:
            continue
        else:
            break
    premises = []
    for i in range(0, len(chosens)-1, 1):
        items = []
        items.append(chosens[i])
        items.append(chosens[i+1])
        random.shuffle(items)
        item1 = items[0]
        item2 = items[1]
        # see if item1 and item2 are in the same group
        if (item1 in group_a and item2 in group_a) or (item1 in group_b and item2 in group_b):
            premise = f"{item1} and {item2} refer to the same person."
            premises.append(premise) 
        else:
            premise = f"{item1} and {item2} are different persons."
            premises.append(premise)
    random.shuffle(premises)
    premises.insert(0, 'Suppose there are only two persons existing.')
    if (chosens[0] in group_a and chosens[-1] in group_a) or (chosens[0] in group_b and chosens[-1] in group_b):
        rconclusion = f"{chosens[0]} and {chosens[-1]} refer to the same person."
        wconclusion = f"{chosens[0]} and {chosens[-1]} refer to different persons."
    else:
        rconclusion = f"{chosens[0]} and {chosens[-1]} are different persons."
        wconclusion = f"{chosens[0]} and {chosens[-1]} refer to the same person."
    if random.choice([True, False]):
        conclusion = rconclusion
        answer = "True"
    else:
        conclusion = wconclusion
        answer = "False"
    argument = premises
    argument.append(conclusion)
    return argument, answer

def separate_into_groups(items):
    group_a = set()
    group_b = set()
    for item in items:
        # Randomly choose a group for each item
        if random.choice([True, False]):
            group_a.add(item)
        else:
            group_b.add(item)
    return group_a, group_b

def get_four_letter_names():
    with open(FOURLETTERNAMESPATH, "r", encoding="utf-8") as f:
        names = f.read().splitlines()
        names = list(set(names))
        return names

if __name__ == "__main__":
    argument, answer = generateOppositeSameQuestions(2)
    print(argument, answer)