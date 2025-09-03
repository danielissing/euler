def compute_P(R, B):
    # Create a 2D DP table
    # dp[r][b] will store P(r, b)
    # We only need even values of r when b is fixed, plus r=0,1

    # Initialize with base cases
    dp = {}

    # Base cases: P(0, b) = 1 for b > 0
    for b in range(B + 1):
        if b > 0:
            dp[(0, b)] = 1.0
        else:
            dp[(0, 0)] = 0.0

    # Base cases: P(r, 0) = 0 for r > 0
    for r in range(R + 1):
        if r > 0:
            dp[(r, 0)] = 0.0

    # Base cases: P(1, b) = 0 for b >= 1
    for b in range(1, B + 1):
        dp[(1, b)] = 0.0

    # Fill the DP table column by column (increasing b)
    for b in range(1, B + 1):
        # For each b, compute P(r, b) for r = 2, 3, ..., R
        for r in range(2, R + 1):
            if (r, b) not in dp:
                # Use the recurrence relation
                # P(r,b) = ((r-1) * P(r-2,b) + 2*b * P(r,b-1)) / (r + 2*b - 1)

                # Get P(r-2, b)
                if r >= 2:
                    p_r2_b = dp.get((r - 2, b), 0.0)
                else:
                    p_r2_b = 0.0

                # Get P(r, b-1)
                p_r_b1 = dp.get((r, b - 1), 0.0)

                # Calculate P(r, b)
                dp[(r, b)] = ((r - 1) * p_r2_b + 2 * b * p_r_b1) / (r + 2 * b - 1)

    return dp[(R, B)]


# Verify with given examples
print(f"P(2,2) = {compute_P(2, 2):.10f}")
print(f"P(10,9) = {compute_P(10, 9):.10f}")
print(f"P(34,25) = {compute_P(34, 25):.10f}")

# Compute the answer
answer = compute_P(24690, 12345)
print(f"\nP(24690,12345) = {answer:.10f}")