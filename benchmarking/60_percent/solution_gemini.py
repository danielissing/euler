import sys


def solve():
    """
    Computes the number of beautiful graphs on 10^7 vertices, G(10^7),
    modulo 10^9 + 7.
    """
    N = 10 ** 7
    MOD = 10 ** 9 + 7

    # T(s): number of 2-edge-colorings of K_s with no monochromatic K_3.
    # T(s) = 0 for s >= 6 by Ramsey's Theorem, R(3,3)=6.
    T_VALUES = [1, 1, 2, 6, 18, 24]  # T(0) to T(5)

    # Precompute factorials and binomial coefficients up to n=5.
    fact = [1] * 6
    for i in range(2, 6):
        fact[i] = fact[i - 1] * i

    C = [[0] * 6 for _ in range(6)]
    for i in range(6):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j])

    # Calculate G(n) and h(n) = G(n)/n! for n = 1 to 5.
    G = [0] * 6
    h = [0] * 6
    G[1] = 1
    h[1] = 1

    for n in range(2, 6):
        g_n = T_VALUES[n]
        for j in range(1, n):
            term = (C[n][j] * T_VALUES[j]) % MOD
            term = (term * G[n - j]) % MOD
            g_n = (g_n + term) % MOD
        G[n] = g_n
        h[n] = (G[n] * pow(fact[n], -1, MOD)) % MOD

    # For n >= 6, h(n) follows a linear recurrence.
    # The coefficients are t_j = T(j)/j!
    t = [0] * 6
    for i in range(1, 6):
        t[i] = (T_VALUES[i] * pow(fact[i], -1, MOD)) % MOD

    # Transition matrix for the recurrence h(n) = t_1*h(n-1) + ... + t_5*h(n-5)
    M = [
        [t[1], t[2], t[3], t[4], t[5]],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
    ]

    def mat_mul(A, B):
        C = [[0] * 5 for _ in range(5)]
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
        return C

    def mat_pow(A, exp):
        res = [[int(i == j) for j in range(5)] for i in range(5)]
        base = A
        while exp > 0:
            if exp % 2 == 1:
                res = mat_mul(res, base)
            base = mat_mul(base, base)
            exp //= 2
        return res

    power = N - 5
    M_pow = mat_pow(M, power)

    # The state vector is S_k = [h(k), h(k-1), ..., h(k-4)]^T
    # We compute S_N = M_pow * S_5
    S5 = [h[5], h[4], h[3], h[2], h[1]]

    h_n = 0
    for i in range(5):
        h_n = (h_n + M_pow[0][i] * S5[i]) % MOD

    # Calculate N! mod MOD for the final step G(N) = h(N) * N!
    fact_n = fact[5]
    for i in range(6, N + 1):
        fact_n = (fact_n * i) % MOD

    result = (h_n * fact_n) % MOD
    print(result)


solve()