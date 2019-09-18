import sys
import math
from sympy import primerange


def find_primes(max):
    primes = []
    if max < 2:
        return primes

    primes.append(2)

    for num in range(3, max):
        flag = True

        for quotient in primes:
            if quotient > math.sqrt(num):
                break

            if num % quotient == 0:
                flag = False
                break

        if flag:
            primes.append(num)

    return primes


def library_method(max):
    return [x for x in primerange(0, max)]


if __name__ == '__main__':
# while True:
#     x = input()
    print(library_method(int(sys.argv[1])))

# print(library_method(int(x)))
