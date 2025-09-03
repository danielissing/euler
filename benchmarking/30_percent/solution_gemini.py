def solve():
    """
    Solves the Project Euler problem by calculating the difference between the sum of
    initial cumulative bean counts and the sum of final (sorted) cumulative bean counts.
    The final state is determined by the lower convex hull of the initial state's
    cumulative sum graph.
    """
    N = 10**7
    MOD = 50515093
    s_initial = 290797

    # Step 1 & 2: Build the convex hull and calculate the sum of initial cumulative sums (sum_CS).
    # This is done in a single pass to optimize memory and time.
    hull = [(-1, 0)]  # Stores (k, C_S[k]) for convex hull vertices. Start with a point (-1, 0).
    sum_CS = 0
    current_CS = 0
    s = s_initial

    for k in range(N):
        # Update cumulative sums with the next value in the sequence
        current_CS += s
        sum_CS += current_CS

        # Maintain the lower convex hull property.
        # The check uses cross-products to avoid floating-point division and handle large numbers.
        # A "right turn" indicates a concavity, so the last point is popped.
        while len(hull) >= 2:
            x1, y1 = hull[-2]
            x2, y2 = hull[-1]
            x3, y3 = k, current_CS
            if (y2 - y1) * (x3 - x2) > (y3 - y2) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append((k, current_CS))

        # Generate the next value in the S_n sequence
        s = (s * s) % MOD

    # Step 3: Compute the sum of the final cumulative sums (sum_CF).
    # This is done by iterating through the segments of the convex hull.
    sum_CF = 0
    for i in range(len(hull) - 1):
        k_i, C_i = hull[i]
        k_i_plus_1, C_i_plus_1 = hull[i + 1]

        dx = k_i_plus_1 - k_i
        dy = C_i_plus_1 - C_i

        if dx == 0:
            continue

        # The final bean counts F_k along a hull segment are almost constant.
        # Their values are either floor(slope) or ceil(slope).
        # This is equivalent to drawing a digital line between hull vertices.
        m = dy // dx
        r = dy % dx
        num_m = dx - r

        # Reconstruct the C_F values along the segment and sum them up.
        current_CF_segment = C_i
        for _ in range(num_m):
            current_CF_segment += m
            sum_CF += current_CF_segment

        for _ in range(r):
            current_CF_segment += m + 1
            sum_CF += current_CF_segment

    # Step 4: The total number of steps is the difference between the two sums.
    result = sum_CS - sum_CF
    print(result)

if __name__ == "__main__":
    solve()
