def xor_product(a, b):
    """Compute the XOR-product of a and b."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def find_solutions(limit):
    """Find all solutions with b <= limit."""
    solutions = []

    # Need to search more thoroughly
    # The equation structure suggests solutions could be larger
    max_search = min(limit + 1, 1000)  # Search up to 1000 or limit

    for a in range(max_search):
        for b in range(a, max_search):
            aa = xor_product(a, a)
            bb = xor_product(b, b)
            ab = xor_product(a, b)
            two_ab = xor_product(2, ab)

            if aa ^ two_ab ^ bb == 5:
                solutions.append((a, b))
                if len(solutions) <= 20:  # Print first 20
                    print(f"Found solution: ({a},{b})")

    return solutions


# Find solutions up to 10
print("Finding solutions with b <= 10:")
solutions_10 = find_solutions(10)

# Calculate X(10)
X_10 = 0
for a, b in solutions_10:
    X_10 ^= b

print(f"\nSolutions with b <= 10: {solutions_10}")
print(f"X(10) = {X_10}")

# Now search more broadly for all solutions
print("\nSearching for all solutions up to 1000:")
all_solutions = find_solutions(1000)

# Group by b value to see pattern
from collections import defaultdict

b_values = defaultdict(list)
for a, b in all_solutions:
    b_values[b].append(a)

print(f"\nTotal solutions found: {len(all_solutions)}")
print("\nB values and their corresponding A values:")
for b in sorted(b_values.keys())[:20]:  # Show first 20 b values
    print(f"  b={b}: a={b_values[b]}")

# Calculate X(10^18)
X_large = 0
for a, b in all_solutions:
    if b <= 10 ** 18:
        X_large ^= b

print(f"\nX(10^18) = {X_large}")