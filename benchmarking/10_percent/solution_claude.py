from math import factorial


def S(k):
    """
    Calculate S(k) = sum of T(n) for all k-digit numbers n,
    where T(n) is the count of permutations of n's digits that are > n.
    """
    total = 0

    # Generate all possible digit multisets (compositions of k into 10 parts)
    def generate_digit_counts(remaining, digit=0):
        """Generate all ways to distribute 'remaining' digits among digits 0-9"""
        if digit == 9:
            yield [remaining]
        else:
            for count in range(remaining + 1):
                for rest in generate_digit_counts(remaining - count, digit + 1):
                    yield [count] + rest

    for counts in generate_digit_counts(k):
        # counts[d] = number of times digit d appears

        # Skip if all digits are 0 (can't form a k-digit number)
        if sum(counts[1:]) == 0:
            continue

        # Calculate number of valid k-digit permutations from this multiset
        # First, total permutations
        total_permutations = factorial(k)
        for c in counts:
            total_permutations //= factorial(c)

        # Subtract permutations with leading zeros
        valid_permutations = total_permutations
        if counts[0] > 0:  # If there are zeros in the multiset
            # Permutations starting with 0
            invalid_permutations = factorial(k - 1)
            invalid_permutations //= factorial(counts[0] - 1)
            for i in range(1, 10):
                invalid_permutations //= factorial(counts[i])
            valid_permutations -= invalid_permutations

        # Each multiset contributes C(valid_permutations, 2) to the sum
        # This counts all pairs (n, m) where n < m within this multiset
        if valid_permutations > 1:
            total += valid_permutations * (valid_permutations - 1) // 2

    return total


# Verify with the given test case
test_result = S(3)
print(f"S(3) = {test_result}")
assert test_result == 1701, f"Test failed: expected 1701, got {test_result}"

# Calculate the answer
answer = S(12)
print(f"\nS(12) = {answer}")

# Brief explanation
print("\n--- Explanation ---")
print("This solution groups k-digit numbers by their digit multisets.")
print("For each multiset, we calculate how many valid k-digit numbers can be formed,")
print("then sum C(count, 2) across all multisets, since within each multiset,")
print("the sum of T(n) equals the number of ordered pairs where one number > another.")
print("\nKey techniques:")
print("- Combinatorial grouping by digit multisets")
print("- Multinomial coefficients for counting permutations")
print("- Efficient generation of integer compositions")
print("- Mathematical insight that sum of T(n) within a group = C(group_size, 2)")