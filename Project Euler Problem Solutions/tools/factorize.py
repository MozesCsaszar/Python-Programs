primes_table = []
file = open('C:\\Users\\ppaa\\Desktop\\My Games\\()Programming\\5_Python\\Challanges\\Project Euler\\tools\\primes_big.txt','r')
#for i in range(664590):
for i in range(1200500):
    primes_table.append(int(file.readline()))
file.close()
def get_nr_factors(factorized):
    to_ret = 1
    for i in range(len(factorized)):
        to_ret *= (factorized[i].power+1)
    return to_ret

def get_sum_divisors(factorized):
    to_ret = 1
    for fac in factorized:
        to_ret *= ((fac.nr**(fac.power+1) - 1)//(fac.nr-1))
    return to_ret

def get_sum_true_divisors(factorized, nr):
    return get_sum_divisors(factorized) - nr

class Factor:
    def __init__(self,nr,power):
        self.nr = nr
        self.power = power

    def __str__(self):
        return str(self.nr) + '^' + str(self.power)

    def __repr__(self):
        return str(self.nr) + '^' + str(self.power)

def factorize(nr):
    factors = [Factor(1,1)]
    i = 0
    old_nr = nr
    while nr != 1 and primes_table[i] <= nr and primes_table[i]*primes_table[i] <= old_nr:
        if nr % primes_table[i] == 0:
            if factors[-1].nr == primes_table[i]:
                factors[-1].power += 1
            else:
                factors.append(Factor(primes_table[i],1))
            nr //= primes_table[i]
        else:
            i += 1
    if nr != 1:
        factors.append(Factor(nr,1))
    return factors[1:]

def get_factors(nr):
    factors = []
    i = 0
    old_nr = nr
    while nr != 1 and primes_table[i]*primes_table[i] <= old_nr:
        if nr % primes_table[i] == 0:
            factors.append(primes_table[i])
            while nr % primes_table[i] == 0:
                nr //= primes_table[i]
        i+=1
    if nr != 1:
        factors.append(nr)
    return factors

def get_phi(nr, factors = []):
    old_nr = nr
    ret = old_nr
    nr = factors
    if nr == []:
        nr = get_factors(nr)
    for i in nr:
        ret = ret*(i-1)
        ret //= i
    return ret
