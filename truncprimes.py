# Truncatable Primes
import math
import random

_mrpt_num_trials = 5  # number of bases to test


def isPrime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    assert n >= 2
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)

    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  # n is definitely composite

    for i in range(_mrpt_num_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False

    return True  # no base tested showed n as composite


def get_left_truncatable_primes():
    candidates = list(range(2, 10))
    left_truncatable_primes = []
    while candidates:
        for candidate in candidates:
            if isPrime(candidate):
                left_truncatable_primes.append(candidate)
                for digit in range(1, 10):
                    test = int(str(digit) + str(candidate))
                    if isPrime(test):
                        left_truncatable_primes.append(test)

                        candidates.append(test)
            candidates.remove(candidate)

    return sorted(list(set(left_truncatable_primes)))


all_lprimes = get_left_truncatable_primes()
print("All left-truncatable primes:")
for prime in all_lprimes:
    print(prime)
print(all([isPrime(num) for num in all_lprimes]))
print("There are {} left-truncatable primes.".format(len(all_lprimes)))
