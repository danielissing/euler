import math


class PermutationSumSolver:
    """
    Solves the Project Euler problem of finding S(k), the sum of T(n)
    for all k-digit numbers n. T(n) is the number of strictly larger
    integers which can be formed by permuting the digits of n.

    The solution is based on a combinatorial approach, iterating over
    digit multisets instead of individual numbers.
    """

    def __init__(self, k):
        """
        Initializes the solver for k-digit numbers.
        """
        self.K = k
        # Pre-compute factorials up to K for efficiency.
        self.fact = [math.factorial(i) for i in range(k + 1)]
        self.total_S = 0

    def _calculate_contribution(self, counts):
        """
        Calculates the contribution for a given multiset of digits.
        The contribution is C(N, 2) where N is the number of unique
        k-digit integers that can be formed from this multiset.
        """

        # Calculate total permutations of the K digits using the multinomial coefficient formula.
        denominator = 1
        for count in counts:
            denominator *= self.fact[count]
        total_perms = self.fact[self.K] // denominator

        # Calculate the number of valid k-digit numbers (no leading zeros).
        num_k_digit_numbers = total_perms

        # If the digit 0 is present (counts[0] > 0), we must subtract permutations
        # that start with 0, as they are not valid k-digit numbers.
        if counts[0] > 0:
            # The number of such invalid permutations is total_perms * (count_of_zeros / K).
            num_k_digit_numbers -= total_perms * counts[0] // self.K

        # The contribution of this multiset is the number of pairs of
        # distinct numbers that can be formed, which is C(N, 2) = N*(N-1)/2.
        if num_k_digit_numbers >= 2:
            self.total_S += num_k_digit_numbers * (num_k_digit_numbers - 1) // 2

    def _generate_multisets(self, k_remaining, digit_idx, counts):
        """
        Recursively generates all multisets of K digits.
        A multiset is represented by the counts of digits 0 through 9.
        """

        # Base case: we are at the last digit (0). The count of digit 0
        # is determined by the remaining number of digits needed.
        if digit_idx == 0:
            counts[0] = k_remaining
            self._calculate_contribution(counts)
            return

        # Recursive step: for the current digit, try all possible counts
        # from 0 up to the number of digits remaining to be chosen.
        for i in range(k_remaining + 1):
            counts[digit_idx] = i
            self._generate_multisets(k_remaining - i, digit_idx - 1, counts)

    def solve(self):
        """
        Runs the solver and returns the final sum S(K).
        """
        # `counts` is an array to store [c0, c1, ..., c9]
        counts = [0] * 10
        # Start generating multisets from digit 9 downwards to build the combinations.
        self._generate_multisets(self.K, 9, counts)
        return self.total_S


def main():
    """
    Main function to solve the problem for S(12) and print the explanation and answer.
    """
    K_VALUE = 12

    # --- Brief Explanation ---
    explanation_summary = (
        "Summary:\n"
        "The problem asks for S(12), the sum of T(n) over all 12-digit numbers n, where T(n) is the count of unique permutations of n's digits that are strictly greater than n. A direct brute-force approach iterating through all 9 * 10^11 numbers is infeasible.\n\n"
        "The key insight is to change the order of summation. Instead of iterating over each number, we iterate over all possible multisets of 12 digits (e.g., {0,0,1,2,3,3,4,5,6,7,8,9}). For any given multiset, let N be the number of distinct 12-digit integers that can be formed. All these N numbers are permutations of each other. The total contribution from this entire group to S(12) is the number of pairs of distinct numbers that can be formed, which is simply N * (N - 1) / 2. Summing these contributions over all possible digit multisets gives the final answer."
    )

    explanation_techniques = (
        "\nKey Math/Coding Techniques:\n"
        "1. Combinatorial Reformulation: The problem is transformed from a sum over ~10^12 numbers to a sum over the ~294,000 unique multisets of 12 digits. This is the crucial optimization.\n"
        "2. Multiset Generation: A recursive function generates all unique multisets (combinations with repetition of 12 items chosen from {0-9}).\n"
        "3. Multinomial Coefficients: The total number of permutations for a multiset with digit counts c_0, ..., c_9 is calculated as 12! / (c_0! * c_1! * ... * c_9!).\n"
        "4. Inclusion-Exclusion Principle: The number of valid integers (N) is found by taking the total number of permutations and subtracting those with an invalid leading zero."
    )

    print(explanation_summary)
    print(explanation_techniques)

    solver = PermutationSumSolver(K_VALUE)
    result = solver.solve()

    print(f"\nThe final answer for S({K_VALUE}) is: {result}")


if __name__ == "__main__":
    main()
