"""
By replacing the 1st digit of the 2-digit number *3, it turns out that six of
the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit
number is the first example having seven primes among the ten generated numbers,
yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993.
Consequently 56003, being the first member of this family, is the smallest prime
with this property.

Find the smallest prime which, by replacing part of the number
(not necessarily adjacent digits) with the same digit, is part of an eight
prime value family.
"""

f = open('primes.txt','r')
primes = {}

nr = int(f.readline())
while nr < 1000000:
    primes[str(nr)] = True
    nr = int(f.readline())
f.close()

def check_nr(nums,i):
    if i == 0:
        return True
    else:
        if i == len(nums) - 1:
            if nums[i] in nums[:i] or nums[i] < nums[i-1]:
                return False
        elif nums[i] in nums[:i] + nums[i+1:] or nums[i] < nums[i-1]:
            return False
    return True

def fill(nr, pos,p):
    if p == len(nr):
        yield nr
    else:
        for i in range(p,len(nr)):
            if i not in pos:
                if i == 0:
                    for j in range(1,10):
                        n_nr = nr.copy()
                        n_nr[i] = j
                        yield from fill(n_nr,pos,i+1)
                else:
                    for j in range(0,10):
                        n_nr = nr.copy()
                        n_nr[i] = j
                        yield from fill(n_nr,pos,i+1)
                break
        else:
            yield nr

def yield_perms(nums,i,maxx):
    if i == len(nums)-1:
        nums[i] = 0
        while nums[i] <= maxx:
            if check_nr(nums,i):
                yield nums
            nums[i] += 1
    else:
        if i != 0:
            nums[i] = 0
        while nums[i] <= maxx:
            if check_nr(nums,i):
                yield from yield_perms(nums.copy(),i+1,maxx)
            nums[i] += 1

def to_str(num,back):
    s = ''
    for i in num:
        s += str(i)
    return s + str(back)

'''
for length in range(5,75):
    print(length-1,'over')
    for i in range(1,length+1):
        nums = []
        for j in range(i):
            nums.append(0)
        nr = []
        for j in range(length):
            nr.append('*')
        for j in yield_perms(nums,0,length-1):
            for fil in fill(nr,j,0):
                n_nr = fil.copy()
                for back in [1,3,7,9]:
                    no_good = 0
                    for k in range(10):
                        for pos in j:
                            if pos == 0 and k == 0:
                                break
                            else:
                                n_nr[pos] = k
                        else:
                            if not primes.get(to_str(n_nr,back)):
                                no_good += 1
                                if no_good >= 3:
                                    break
                    else:
                        if fil[0] == '*' and no_good == 1:
                            print(to_str(fil,back))
                        elif no_good == 2:
                            print(to_str(fil,back))

'''
for i in fill(['*',2,'*',3,'*'],[1,3],0):
    if primes.get(to_str(i,3)):
        print(to_str(i,3))
        break


