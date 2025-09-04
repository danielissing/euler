import math
from collections import defaultdict


def solve_for_d(a, b, c, n):
    """
    Given a, b, c, find valid d values such that:
    - c <= d <= n
    - a^2 + b^2 + c^2 + d^2 = (a+b+c+d)(a+b+c+d+2)/4
    """
    s3 = a + b + c
    sq3 = a * a + b * b + c * c

    # Quadratic equation: 3d^2 - 2(s3+1)d - (s3^2 + 2s3 - 4sq3) = 0
    # Discriminant = 16s3^2 + 32s3 + 4 - 48sq3
    discriminant = 16 * s3 * s3 + 32 * s3 + 4 - 48 * sq3

    if discriminant < 0:
        return []

    sqrt_disc = math.isqrt(discriminant)
    if sqrt_disc * sqrt_disc != discriminant:
        return []

    # Check both solutions
    valid_d = []
    numerator1 = 2 * (s3 + 1) + sqrt_disc
    numerator2 = 2 * (s3 + 1) - sqrt_disc

    for num in [numerator1, numerator2]:
        if num % 6 == 0:
            d = num // 6
            if c <= d <= n:
                # Verify the constraint
                s = s3 + d
                if 4 * (sq3 + d * d) == s * (s + 2):
                    valid_d.append(d)

    return valid_d


def compute_S(n, modulo=None):
    """
    Optimized computation of S(n).
    Uses mathematical constraints to reduce search space.
    """
    total = 0
    count = 0

    # Key optimization: limit the range of a based on the fact that
    # for (a,a,a,a), we have 4a^2 = 4a(4a+2)/4 = a(4a+2)
    # This gives 4a = 4a+2, which is impossible
    # So we need at least some variation in values

    max_a = n

    for a in range(1, min(max_a + 1, n + 1)):
        # Early termination based on minimum possible sum
        if 4 * a > 4 * n:
            break

        for b in range(a, n + 1):
            # More aggressive pruning
            if a + 3 * b > 4 * n:
                break

            for c in range(b, n + 1):
                # Check if minimum possible d would exceed n
                if a + b + 2 * c > 4 * n:
                    break

                # Find valid d values
                valid_d = solve_for_d(a, b, c, n)

                for d in valid_d:
                    s = a + b + c + d
                    count += 1
                    if modulo:
                        total = (total + s) % modulo
                    else:
                        total += s

    return total, count


def find_pattern(max_n=100):
    """Look for patterns in S(n) that might help with larger values."""
    print("Looking for patterns in S(n):")
    results = []
    for n in [5, 10, 20, 50, 100]:
        s, c = compute_S(n)
        results.append((n, s, c))
        print(f"S({n:3}) = {s:10}, count = {c:6}")
    return results


# Verification
print("=== Verification ===")
s5, c5 = compute_S(5)
print(f"S(5) = {s5} (expected: 48), count = {c5} (expected: 5)")

print("\n=== Testing larger values ===")
s1000, c1000 = compute_S(1000)
print(f"S(1000) = {s1000} (expected: 37048340), count = {c1000}")

# Look for patterns
print("\n=== Pattern Analysis ===")
pattern_results = find_pattern()

# For S(10^8), we need a different approach
print("\n=== Attempting S(10^8) ===")
print("Note: Direct computation would take too long.")
print("We need one of these approaches:")
print("1. Mathematical closed form or recurrence relation")
print("2. Number theoretic insights about the constraint")
print("3. Parallel computation with optimized C++ implementation")

# Let's at least try a larger value with modulo
n_large = 100000  # Still much smaller than 10^8
modulo = 433494437
print(f"\nComputing S({n_large}) mod {modulo} as a test...")
s_large, c_large = compute_S(n_large, modulo)
print(f"S({n_large}) ≡ {s_large} (mod {modulo})")
print(f"Number of quadruples: {c_large}")

# Additional optimization idea: caching and symmetry
print("\n=== Optimization Ideas ===")
print("For S(10^8), consider:")
print("- The constraint creates a sparse set of valid quadruples")
print("- Possible parametric solution using number theory")
print("- The discriminant condition severely limits valid combinations")
print("- May need to find a generating function or use FFT-based convolution")