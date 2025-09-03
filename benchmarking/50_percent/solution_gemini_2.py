import sys
import math
import random
from collections import defaultdict
from functools import lru_cache

# Set a higher recursion limit for deep searches.
sys.setrecursionlimit(2000)

MOD = 409120391


# --- Miller-Rabin Primality Test ---
def power(a, b, m):
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res


def is_prime(n, k=5):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


# --- Pollard's Rho Integer Factorization ---
def pollard_rho(n):
    if is_prime(n): return n
    if n % 2 == 0: return 2
    x = random.randint(1, n - 2)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    while d == 1:
        x = ((x * x) % n + c + n) % n
        y = ((y * y) % n + c + n) % n
        y = ((y * y) % n + c + n) % n
        d = math.gcd(abs(x - y), n)
        if d == n:
            return pollard_rho(n)
    return d


@lru_cache(maxsize=None)
def get_factors(n):
    if n == 1: return {}
    factors = defaultdict(int)
    num = n
    while num > 1:
        if is_prime(num):
            factors[num] += 1
            break
        factor = pollard_rho(num)
        sub_factors1 = get_factors(factor)
        for p, e in sub_factors1.items(): factors[p] += e
        sub_factors2 = get_factors(num // factor)
        for p, e in sub_factors2.items(): factors[p] += e
        break
    return dict(factors)


# --- Primes pre-computation ---
P1_PRIMES = []
P3_PRIMES = []


def sieve_primes(limit):
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for p in range(2, limit + 1):
        if is_p[p]:
            if p > 2:
                if p % 4 == 1:
                    P1_PRIMES.append(p)
                else:
                    P3_PRIMES.append(p)
            for i in range(p * p, limit + 1, p):
                is_p[i] = False


sieve_primes(500)  # Increased slightly to be safe
P1_PRIMES_TUPLE = tuple(P1_PRIMES)
P3_PRIMES_TUPLE = tuple(P3_PRIMES)


# --- Optimized `min_num_creator` ---
# This function finds the smallest number `m` by factorizing `d` and
# optimally assigning exponents to the smallest primes of the correct type.
@lru_cache(maxsize=None)
def min_num_creator_optimized(d, primes_tuple):
    if d == 1: return 1

    factors_of_d = get_factors(d)

    prime_factors_list = []
    for p, e in factors_of_d.items():
        prime_factors_list.extend([p] * e)

    exponents = sorted([(q - 1) // 2 for q in prime_factors_list], reverse=True)

    primes = list(primes_tuple)
    if len(exponents) > len(primes):
        return float('inf')

    res = 1
    for i in range(len(exponents)):
        base = primes[i]
        exp = exponents[i]
        # Heuristic check to prevent trying to compute enormous numbers
        if exp > 0 and math.log(base) * exp > 100:
            return float('inf')
        term = pow(base, exp)
        if res > float('inf') / term:  # Check for overflow before multiplying
            return float('inf')
        res *= term

    return res


# --- Helper functions for iterating divisors and factors ---
def get_divisors_from_factors(factors_dict):
    divs = [1]
    for p, e_max in factors_dict.items():
        new_divs = []
        for i in range(e_max + 1):
            for d in divs:
                new_divs.append(d * (p ** i))
        divs = new_divs
    return divs


# --- Main solver function ---
def find_q(N):
    target = 2 * N + 2
    min_overall_n = float('inf')

    target_odd_part = target
    while target_odd_part % 2 == 0:
        target_odd_part //= 2

    target_odd_factors = get_factors(target_odd_part)
    odd_divisors_of_target = get_divisors_from_factors(target_odd_factors)

    # Precompute n1 values as d1 is used repeatedly
    n1_map = {d1: min_num_creator_optimized(d1, P1_PRIMES_TUPLE) for d1 in odd_divisors_of_target}

    for d1 in odd_divisors_of_target:
        n1 = n1_map[d1]
        if n1 == float('inf'): continue

        Y = target // d1

        # Case 1: n is odd (k=0)
        if Y % 2 == 0:
            d3 = Y - 1
            if d3 > 0:
                n3 = min_num_creator_optimized(d3, P3_PRIMES_TUPLE)
                if n3 != float('inf'):
                    min_overall_n = min(min_overall_n, n1 * n3)

        # Case 2: n is even (k>0)
        if Y % 2 == 0:
            Y1 = Y - 1
            if Y1 > 0:
                Y1_divs = get_all_divisors(Y1)
                for D in Y1_divs:
                    if D % 2 == 1:
                        k_val = (D + 1) // 2

                        # Heuristic prune: if k_val is too large, 2^k_val will dominate
                        # and this path is unlikely to yield a minimum. A cap of 100 is
                        # conservative, as 2^100 is enormous. This prevents both long
                        # pow() computations and the subsequent float OverflowError.
                        if k_val > 100:
                            continue

                        d3 = Y1 // D
                        n3 = min_num_creator_optimized(d3, P3_PRIMES_TUPLE)
                        if n3 != float('inf'):
                            term_2k = pow(2, k_val)

                            # The original float-based overflow check was the source of the
                            # error. Python's arbitrary precision integers can handle the
                            # multiplication, so we just compare the result to the minimum.
                            min_overall_n = min(min_overall_n, term_2k * n1 * n3)
    return min_overall_n


@lru_cache(maxsize=None)
def get_all_divisors(n):
    factors = get_factors(n)
    return get_divisors_from_factors(factors)


def main():
    total_sum = 0
    for k_exp in range(1, 19):
        N = 10 ** k_exp
        Q_N = find_q(N)
        total_sum = (total_sum + Q_N) % MOD

    print("The final answer is:")
    print(total_sum)


if __name__ == "__main__":
    main()


