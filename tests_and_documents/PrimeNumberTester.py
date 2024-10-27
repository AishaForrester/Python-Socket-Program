from NumTheory import NumTheory
import math


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if NumTheory.expMod(n,1,2) == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def tester():
    n = int(input("Enter a prime number: "))
    if is_prime(n):
        print("This number is a prime")
    else:
        print("This number is not a prime")

tester()

