# Truncatable Primes
import math
import random
import matplotlib.pyplot as plt
_mrpt_num_trials = 5  # number of bases to test


def isPrime(n):
    """
    Taken from https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python:_Probably_correct_answers

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


def get_truncatable_primes(left_or_right):
    candidates = list(range(2, 10))
    left_truncatable_primes = []
    while candidates:
        for candidate in candidates:
            if isPrime(candidate):
                left_truncatable_primes.append(candidate)
                for digit in range(1, 10):
                    if left_or_right == "left":
                        test = int(str(digit) + str(candidate))
                    else:
                        test = int(str(candidate) + str(digit))
                    if isPrime(test):
                        left_truncatable_primes.append(test)

                        candidates.append(test)
            candidates.remove(candidate)

    return sorted(list(set(left_truncatable_primes)))


def get_digit_breakdown(all_primes):
    digit_counts = {}
    for length in range(len(str(max(all_primes)))):
        digit_counts[length] = len(
            list(filter(lambda x: len(str(x)) == length, all_primes)))
    return digit_counts


for direction in ["left", "right"]:
    all_primes = get_truncatable_primes(direction)
    print("All {}-truncatable primes:".format(direction))
    # print(*all_primes, sep="\n")
    print("There are {} {}-truncatable primes.".format(len(all_primes), direction))

    digit_dict = get_digit_breakdown(all_primes)
    plt.bar(range(1, len(digit_dict) + 1),
            list(digit_dict.values()), align='center')
    plt.xticks(range(1, len(digit_dict) + 1),
               list(map(lambda x: x + 1, digit_dict.keys())))
    plt.xlabel("Number of digits")
    plt.ylabel("Count")
    plt.title(
        "Distribution of X-digit {}-truncatable primes".format(direction.capitalize()))
    plt.show()
