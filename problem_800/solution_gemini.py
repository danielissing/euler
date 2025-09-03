import math

def solve_euler_problem():
    """
    Solves the Euler problem to find C(800800^800800).

    The problem asks for the number of "hybrid-integers" less than or equal to a given number n.
    A hybrid-integer is of the form p^q * q^p, where p and q are distinct prime numbers.
    C(n) is the count of such integers. We need to find C(800800^800800).

    The method uses logarithms to handle the large numbers and an efficient two-pointer
    algorithm to count the valid prime pairs.
    """

    # Define the constants from the problem.
    base = 800800
    exponent = 800800

    # Calculate the natural logarithm of n = base^exponent.
    # log(n) = exponent * log(base)
    log_n = exponent * math.log(base)

    # Estimate the upper limit for primes needed. The largest prime in a pair
    # will occur when the other prime is the smallest, i.e., p=2.
    # The inequality becomes q*log(2) + 2*log(q) <= log_n.
    # For large q, q*log(2) dominates, so q is approximately log_n / log(2).
    # This gives q ~ 1.57e7. We'll use a safe upper bound.
    prime_limit = 16000000

    # Step 1: Generate primes using a Sieve of Eratosthenes.
    print(f"Generating primes up to {prime_limit}...")
    is_prime = [True] * (prime_limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(prime_limit)) + 1):
        if is_prime[i]:
            for multiple in range(i * i, prime_limit + 1, i):
                is_prime[multiple] = False

    primes = [i for i, is_p in enumerate(is_prime) if is_p]
    print(f"Found {len(primes)} primes.")

    # Pre-calculate logarithms of primes for efficiency.
    log_primes = [math.log(p) for p in primes]

    # Step 2: Use the two-pointer algorithm to count valid pairs (p, q) with p < q.
    count = 0
    i = 0  # Pointer for the smaller prime p
    j = len(primes) - 1  # Pointer for the larger prime q

    print("Counting hybrid-integer pairs...")
    while i < j:
        p = primes[i]
        q = primes[j]
        log_p = log_primes[i]
        log_q = log_primes[j]

        # Check the inequality: q*log(p) + p*log(q) <= log_n
        if q * log_p + p * log_q <= log_n:
            # If (p, q) is a valid pair, then p combined with any prime
            # between p and q is also valid, because the function
            # f(x) = x*log(p) + p*log(x) is monotonically increasing.
            # The number of such primes is (j - 1) - (i + 1) + 1 = j - i.
            count += (j - i)
            # We have found all pairs for this p, so move to the next p.
            i += 1
        else:
            # If the pair is not valid, q is too large for this p.
            # Try a smaller q.
            j -= 1

    print(f"\nCalculation complete.")
    print(f"The value of C(800800^800800) is: {count}")


# Run the solver function
solve_euler_problem()