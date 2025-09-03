# Computes B(10^7) for the bean-moving process with S_{n+1} = S_n^2 mod 50515093
# Strategy:
#   1) PAVA on S_i to get convex cumulative (non-decreasing slopes) in blocks.
#   2) Integer-ize block slopes with a second merging pass.
#   3) B = sum_i i*(A*_i - S_i) = P_final - P_initial.

def main():
    N = 10_000_000
    MOD = 50515093
    x = 290_797

    # PAVA stacks: each entry is a block with (length, total)
    lens = []
    sums = []

    # Pre-bind methods for speed
    lens_append = lens.append
    sums_append = sums.append

    # Initial potential sum \sum i*S_i
    P_init = 0

    # Generate S_i and do PAVA in one streaming pass
    for i in range(N):
        s = x
        P_init += i * s

        lens_append(1)
        sums_append(s)

        # Merge while last two blocks violate non-decreasing averages
        # Compare avg_prev <= avg_last via cross-multiplication
        while len(lens) >= 2:
            L2 = lens[-1]; T2 = sums[-1]
            L1 = lens[-2]; T1 = sums[-2]
            # If avg_prev > avg_last then merge
            if T1 * L2 > T2 * L1:
                # merge blocks (L1,T1) and (L2,T2) into position -2
                lens[-2] = L1 + L2
                sums[-2] = T1 + T2
                lens.pop()
                sums.pop()
            else:
                break

        x = (x * x) % MOD

    # Second pass: enforce that after integer rounding, slopes stay non-decreasing across blocks.
    # For a block (L,T), slopes will be:
    #   q = T//L repeated (L-r) times, then q+1 repeated r times, where r = T%L.
    # To guarantee global monotonicity, ensure ceil(left_avg) <= floor(right_avg).
    Ls = []
    Ts = []
    Ls_append = Ls.append
    Ts_append = Ts.append

    for L, T in zip(lens, sums):
        Ls_append(L); Ts_append(T)
        # While the integerized max of previous block exceeds the integerized min of current, merge
        while len(Ls) >= 2:
            L2 = Ls[-1]; T2 = Ts[-1]
            L1 = Ls[-2]; T1 = Ts[-2]
            q1, r1 = divmod(T1, L1)
            max_left = q1 + (1 if r1 else 0)          # last slope in left block
            q2 = T2 // L2                              # first slope in right block
            if max_left > q2:
                # Merge into the left position
                Ls[-2] = L1 + L2
                Ts[-2] = T1 + T2
                Ls.pop(); Ts.pop()
            else:
                break

    # Compute P_final = sum_i i * A*_i from the finalized integer blocks.
    # For a block starting at index 'start' of length L with T = q*L + r:
    #   slopes: q for first (L-r) indices, q+1 for last r indices.
    # Contribution = q * sum_{i=start}^{start+L-1} i + sum_{i=start+L-r}^{start+L-1} i
    def sum_indices(a, b):
        if b < a:
            return 0
        n = b - a + 1
        return n * (a + b) // 2

    P_final = 0
    start = 0
    for L, T in zip(Ls, Ts):
        q, r = divmod(T, L)
        # sum of all indices in this block
        block_sum = sum_indices(start, start + L - 1)
        P_final += q * block_sum
        if r:
            # sum of last r indices in the block
            P_final += sum_indices(start + L - r, start + L - 1)
        start += L

    # Number of steps
    B = P_final - P_init
    print(B)

if __name__ == "__main__":
    main()
