"""
The cube, 41063625 (345^3), can be permuted to produce two other cubes:
56623104 (384^3) and 66430125 (405^3). In fact, 41063625 is the smallest cube
which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are
cube.
"""


def get_repr(nr):
    nr = str(nr)
    n_nr = [0,0,0,0,0,0,0,0,0,0]
    for i in nr:
        n_nr[int(i)] += 1
    return tuple(n_nr)

i = 1

cubes = {}

while True:
    i += 1
    nr = i*i*i
    n_nr = get_repr(nr)
    if cubes.get(n_nr):
        cubes[n_nr][1] += 1
        if cubes[n_nr][1] == 5:
            print(cubes[n_nr][0])
            break
    else:
        cubes[n_nr] = [nr,1]
