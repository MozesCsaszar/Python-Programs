"""
Consider the fraction, n/d, where n and d are positive integers. If n<d and
HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of
size, we get:
1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7,
3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 21 elements in this set.

How many elements would be contained in the set of reduced proper fractions for
d ≤ 1,000,000?
"""


from tools.factorize import get_factors, get_phi, primes_table


#solved with a sieve
d = int(input("d <= as "))

def calc_things(factors, start_i, bound, p):
    for i in range(start_i, len(factors)):
        if factors[i] * p <= bound:
            if start_i > 0:
                yield factors[i] * p
            yield from calc_things(factors, i + 1, bound, factors[i] * p)
            
def calc_nr_to_add(factors, bound):
    to_ret = 0
    if len(factors) == 1:
        return bound
    for i in factors:
        to_ret += bound//i
    for i in calc_things(factors,0,bound,1):
        to_ret -= bound//i
    return bound - to_ret

nr = d - 1

#use some math magic to make it faster
for i in range(2,d):
    factors = get_factors(i)
    p_nr = d - i
    nr += (p_nr//i)*get_phi(i,factors)
    nr += calc_nr_to_add(factors,p_nr%i)
    if(i % 100000 == 0):
        print(i)

print(nr)
            

