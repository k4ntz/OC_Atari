import numpy as np

a, b, c = 1, 2, 3
list = [a, b, c]
# print(np.delete(list, [0, 2]))
print(list)

list_1 = [[1, 2, 3, 4], [1, 5, 7, 8]]
list_2 = []
list_2.extend(alien for l in list_1 for alien in l if isinstance(alien, int))
print(list_2)

del list[0:0]
print(list)
# for i in range(3):
#     for j in range(6):
#         print(list[i] % pow(2, j+1) >= pow(2, j))

# for i in range(3):
#     if list[i] == 2:
#         del list[i]