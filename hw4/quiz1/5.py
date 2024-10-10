<<<<<<< HEAD
def rail_fence_cipher(a, group_size):
    return ''.join(a[i::group_size] for i in range(group_size))

a = input("enter the message to encrypt: ")
group_size = int(input("enter the group size (e.g., 3 for groups of three): "))
print(rail_fence_cipher(a, group_size))
