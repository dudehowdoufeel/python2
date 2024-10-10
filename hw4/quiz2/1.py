
def swap(w1, w2):
    swapped_w1 = w2[0] + w1[1:]
    swapped_w2 = w1[0] + w2[1:]
    return swapped_w1, swapped_w2

w1 = "kbtu"
w2 = "mkm"
swapped = swap(w1, w2)
print(swapped)
#jg

