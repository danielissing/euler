import sys


def solve():
    """
    Solves Project Euler Problem 579 using dynamic programming.

    The problem asks for P(R, B), the probability that a card game ends with only
    black cards. The state is (r, b), the number of red and black cards.

    A recurrence relation for the probability P(r, b) can be derived:
    P(r, b) = (r-1)/(r+2b-1) * P(r-2, b) + 2b/(r+2b-1) * P(r, b-1)

    Since r always decreases by 2, we can define dp[i][j] = P(2i, j), where
    i = r/2. The recurrence becomes:
    dp[i][j] = ((2i-1)*dp[i-1][j] + 2j*dp[i][j-1]) / (2i+2j-1)

    Base cases:
    - P(0, b) = 1 for b > 0 (no red cards left) => dp[0][j] = 1
    - P(r, 0) = 0 for r > 0 (no black cards left) => dp[i][0] = 0

    We compute this using DP, optimizing memory by only storing the previous
    and current rows for the 'i' dimension.
    """
    R = 24690
    B = 12345

    I = R // 2

    # dp corresponds to the row for i-1 (previous)
    # dp_next corresponds to the row for i (current)

    # Initialize dp for the base case i=0
    dp = [0.0] * (B + 1)
    for j in range(1, B + 1):
        dp[j] = 1.0

    dp_next = [0.0] * (B + 1)

    # Iterate through i from 1 to I (representing r=2, 4, ..., R)
    for i in range(1, I + 1):
        # Base case dp_next[0] = P(2i, 0) = 0
        dp_next[0] = 0.0
        # Iterate through j from 1 to B (representing b=1, 2, ..., B)
        for j in range(1, B + 1):
            numerator = (2 * i - 1) * dp[j] + (2 * j) * dp_next[j - 1]
            denominator = 2 * i + 2 * j - 1
            dp_next[j] = numerator / denominator

        # Swap arrays for the next iteration to avoid expensive copying.
        # dp_next now holds the results for row i, and it will become the 'previous'
        # row (dp) for the i+1 iteration. The old dp array is used as scratch
        # space for dp_next in the next iteration. This is much more efficient.
        dp, dp_next = dp_next, dp

    # After the loop, dp holds the final row of probabilities for i=I
    final_probability = dp[B]

    print(f"The value of P({R},{B}) is: {final_probability:.10f}")


if __name__ == "__main__":
    solve()

