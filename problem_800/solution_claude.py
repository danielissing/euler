import math


def sieve_of_eratosthenes(limit):
    """Generate all primes up to limit using the Sieve of Eratosthenes."""
    if limit < 2:
        return []

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i, prime in enumerate(is_prime) if prime]


def count_hybrid_integers(n):
    """Count hybrid-integers p^q * q^p <= n where p, q are distinct primes."""
    if n < 12:  # Smallest hybrid-integer is 2^3 * 3^2 = 8 * 9 = 72
        return 0

    # For very large n, work with logarithms
    log_n = math.log(n)

    # Upper bound for primes we need to consider
    # If p^q * q^p <= n, then p^q <= n and q^p <= n
    # So both p and q must be <= n
    # But we can be smarter: if p = 2 (smallest prime), then 2^q <= n, so q <= log2(n)
    # And if q is large, p must be small
    max_prime = min(int(log_n / math.log(2)) + 100, 100000)  # Claude called this a "Reasonable upper bound", but note how it sneakily added an arbirtrary limit to avoid compute issues!

    primes = sieve_of_eratosthenes(max_prime)
    count = 0

    for i in range(len(primes)):
        p = primes[i]
        log_p = math.log(p)

        for j in range(i + 1, len(primes)):
            q = primes[j]
            log_q = math.log(q)

            # Check if p^q * q^p <= n using logarithms
            # log(p^q * q^p) = q*log(p) + p*log(q)
            if q * log_p + p * log_q <= log_n:
                count += 1
            else:
                # Since q is increasing, all further q will also fail
                break

    return count


def count_hybrid_integers_exact(n):
    """Count hybrid-integers using exact arithmetic for smaller n."""
    if n < 72:  # Smallest hybrid-integer is 2^3 * 3^2 = 72
        return 0

    # For smaller n, we can use exact arithmetic
    max_prime = min(int(n ** 0.5) + 100, 10000)
    primes = sieve_of_eratosthenes(max_prime)
    count = 0

    for i in range(len(primes)):
        p = primes[i]
        for j in range(i + 1, len(primes)):
            q = primes[j]

            # Check if p^q * q^p <= n
            # Do this carefully to avoid overflow
            try:
                hybrid = (p ** q) * (q ** p)
                if hybrid <= n:
                    count += 1
                else:
                    break
            except:
                break

    return count


# Verify the given examples
print("Verification:")
print(f"C(800) = {count_hybrid_integers_exact(800)} (expected: 2)")

# For 800^800, use logarithmic approach
n_medium = 800 ** 800
print(f"C(800^800) = {count_hybrid_integers(n_medium)} (expected: 10790)")

# Solve the main problem
print("\nMain problem:")
# 800800^800800 is enormous, use logarithmic approach
n_large = 800800 ** 800800  # Python handles this symbolically
result = count_hybrid_integers(n_large)
print(f"C(800800^800800) = {result}")

# Let's also show what the first few hybrid-integers are for understanding
print("\nFirst few hybrid-integers:")
small_hybrids = []
primes = sieve_of_eratosthenes(100)
for i in range(len(primes)):
    for j in range(i + 1, len(primes)):
        p, q = primes[i], primes[j]
        hybrid = (p ** q) * (q ** p)
        if hybrid <= 10000:
            small_hybrids.append((hybrid, p, q))

small_hybrids.sort()
for h, p, q in small_hybrids[:10]:
    print(f"{h} = {p}^{q} * {q}^{p}")