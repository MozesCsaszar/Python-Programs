def from_base_10_to_binary(number):
    if number == 0:
        return '0'
    elif number == 1:
        return '1'
    else:
        return from_base_10_to_binary(number//2) + str(number%2)

def from_binary_to_base_10(number):
    number = str(number)
    new_nr = 0
    for i in range(len(number)):
        new_nr += 2**i*int(number[i])
    return new_nr

def from_base_a_to_base_b(number,base_a,base_b):
    '''base_a is the base of the number, base_b is the base of the result'''
    number = str(number)
    def from_base_a_to_base_10():
        if base_a == 10:
            return number
        new_nr = 0
        for i in range(len(number)):
            new_nr += base_a**i*int(number[i])
        return new_nr
    number = int(from_base_a_to_base_10())
    def from_base_10_to_base_b(number):
        if number < base_b:
            return str(number)
        else:
            return  from_base_10_to_base_b(number//base_b) + str(number%base_b)
    return from_base_10_to_base_b(number)
    
