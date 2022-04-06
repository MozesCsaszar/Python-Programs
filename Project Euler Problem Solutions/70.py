"""
Euler's Totient function, φ(n) [sometimes called the phi function], is used to
determine the number of positive numbers less than or equal to n which are
relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than
nine and relatively prime to nine, φ(9)=6.
The number 1 is considered to be relatively prime to every positive number, so
φ(1)=1.

Interestingly, φ(87109)=79180, and it can be seen that 87109 is a permutation of
79180.

Find the value of n, 1 < n < 107, for which φ(n) is a permutation of n and the
ratio n/φ(n) produces a minimum.
"""


import tools.factorize as f

def calc_digs(nr):
    nr = str(nr)
    ret = [0,0,0,0,0,0,0,0,0,0]
    for i in nr:
        ret[int(i)] += 1
    return ret

maxx = 2
n = 0

j = 78497

j = 0
nr = 0
phi_nr = 0

def yield_nrs(nr,facts,i,maxx):
    if nr < maxx:
        while f.primes_table[i] * nr < maxx:
            n_facts = facts.copy()
            n_facts.append(f.primes_table[i])
            yield (nr*f.primes_table[i],n_facts)
            yield from yield_nrs(nr*f.primes_table[i],n_facts,i+1,maxx)
            i += 1
            
for j in yield_nrs(1,[1],0,21):
    print(j)

for nr in yield_nrs(1,[],0,10**7):
    phi_nr = f.get_phi(nr[0],nr[1])
    nr = nr[0]
    if calc_digs(nr) == calc_digs(phi_nr):
        if nr/phi_nr < maxx:
            n = nr
            maxx = nr/phi_nr
        
    
        

print(n)
