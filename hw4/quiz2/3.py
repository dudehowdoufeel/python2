def find_strings(L, pattern):
    pattern_dict = {i: char for i, char in enumerate(pattern) if char != '*'}
    matching = []
    
    for s in L:
        if len(s) != len(pattern):
            continue
        match = True
        for index, char in pattern_dict.items():
            if s[index] != char:
                match = False
                break
        if match:
            matching(s)
    return matching

L = ['aabaabac', 'cabaabca', 'aaabbcba', 'aabacbab', 'acababba']
a = input("enter your pattern and * for unknown chars): ")
results = find_strings(L, a)
print(results)
