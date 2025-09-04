import math

# -------- prime generation: odd-only sieve (memory & speed friendly) --------
def sieve_primes_upto(n: int):
    """Return list of all primes <= n using an odd-only sieve."""
    if n < 2:
        return []
    # Number of odd integers in [3..n]
    size = (n - 1) // 2
    sieve = bytearray(b'\x01') * size
    limit = int(math.isqrt(n))
    # index i corresponds to number p = 2*i + 3
    for i in range((limit - 1)//2 + 1):
        if sieve[i]:
            p = 2*i + 3
            start = (p*p - 3)//2
            sieve[start::p] = b'\x00' * ((size - start - 1)//p + 1)
    return [2] + [2*i + 3 for i in range(size) if sieve[i]]

# -------- core counting in log-space with a two-pointer sweep --------
def count_hybrids_with_logL(L: float) -> int:
    """
    Count hybrid-integers <= e^L, i.e. unordered prime pairs (p<q) with
    q*ln(p) + p*ln(q) <= L.
    """
    # For any p>=2, q*ln p >= q*ln 2, so q <= L/ln 2 is a safe global cap.
    q_cap = int(L / math.log(2)) + 1

    primes = sieve_primes_upto(q_cap)
    logs = [math.log(p) for p in primes]

    total = 0
    j = len(primes) - 1
    eps = 1e-12  # tiny slack for floating-point comparisons

    # sweep p = primes[i], keep shrinking j so that inequality holds
    for i, p in enumerate(primes):
        if i == len(primes) - 1:
            break
        lp = logs[i]
        # move j down until q*ln p + p*ln q <= L
        while j > i and primes[j] * lp + p * logs[j] > L + eps:
            j -= 1
        if j <= i:
            break
        total += (j - i)
    return total

def C_upto(n: int) -> int:
    """C(n) with n small enough to take math.log(n) directly."""
    return count_hybrids_with_logL(math.log(n))

def C_power(base: int, exp: int) -> int:
    """C(base^exp) without constructing the huge number: uses exp*ln(base)."""
    return count_hybrids_with_logL(exp * math.log(base))

if __name__ == "__main__":
    # Given checks
    print("C(800) =", C_upto(800))                       # expected 2
    print("C(800^800) =", C_power(800, 800))             # expected 10790

    # The target
    ans = C_power(800_800, 800_800)
    print("C(800800^800800) =", ans)
