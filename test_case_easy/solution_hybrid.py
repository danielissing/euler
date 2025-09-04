import math

# -------- prime generation: odd-only sieve --------
def sieve_primes_upto(n: int):
    """Return list of all primes <= n using an odd-only sieve of Eratosthenes."""
    if n < 2:
        return []
    # Number of odd integers in [3..n]
    size = (n - 1) // 2
    sieve = bytearray(b'\x01') * size  # more memory-efficient than list of booleans
    limit = int(math.isqrt(n))
    # index i corresponds to number p = 2*i + 3
    for i in range((limit - 1)//2 + 1):
        if sieve[i]:
            p = 2*i + 3
            start = (p*p - 3)//2
            sieve[start::p] = b'\x00' * ((size - start - 1)//p + 1) # faster than looping as it marks all multiples at once
    return [2] + [2*i + 3 for i in range(size) if sieve[i]] # add 2 by hand as it's the only even prime


# -------- core counting in log-space with a two-pointer approach --------
def count_hybrids_with_logL(L: float) -> int:
    """
    Count hybrid-integers <= e^L, i.e. unordered prime pairs (p<q) with
    q*ln(p) + p*ln(q) <= L.
    """
    # For any p>=2, q*ln p >= q*ln 2, so q <= L/ln 2 is a safe global cap.
    q_cap = int(L / math.log(2)) + 1

    primes = sieve_primes_upto(q_cap)
    log_primes = [math.log(p) for p in primes]

    total = 0
    i = 0 # use i as a pointer for the smaller prime p
    j = len(primes) - 1 # j is the pointer for prime q
    epsilon = 1e-12  # tiny slack for floating-point comparisons

    while i < j:
        p = primes[i]
        q = primes[j]
        log_p = log_primes[i]
        log_q = log_primes[j]

        # Check the inequality: q*log(p) + p*log(q) <= log_n
        if q * log_p + p * log_q <= L + epsilon:
            # If (p, q) is a valid pair, then p combined with any prime
            # between p and q is also valid
            # The number of such primes is (j - 1) - (i - 1) = j - i.
            total += (j - i)
            # We have found all pairs for this p, so move to the next p.
            i += 1
        else:
            # If the pair is not valid, q is too large for this p.
            j -= 1
    return total

def brute_force_solution(n: int) -> int:

    # find all prime numbers smaller than n
    primes = []
    for i in range(2,n):
        is_prime = True
        for j in range(2,i):
            if i%j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)

    final_result = 0 # set up counter

    # loop through all pairs (p,q) in the list of primes with q<p and check if they satisfy condition
    for j in range (1,len(primes)-1):
        for k in range(0,j):
            p = primes[j]
            q = primes[k]
            if (p ** q) * (q ** p) <=n:
                final_result +=1

    return final_result

if __name__ == "__main__":
    # Verify examples
    print("Verifying provided examples:\n")
    ex_1 = count_hybrids_with_logL(math.log(800))
    ex_2 = count_hybrids_with_logL(800 * math.log(800))
    print(f"C(800) = {ex_1}, expected 2.")
    print(f"C(800^800) = {ex_2}, epxected 10790.\n")

    # Finding the solution
    ans = count_hybrids_with_logL(800_800 * math.log(800_800))
    print("The solution to the problem is C(800800^800800) =", ans)
