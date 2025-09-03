# Dynamical polynomials: S(10000) mod 998244353
# Correct, fast solution with small-case checks.
#
# Math outline:
# Let x = t + t^{-1}. Then x^2 - 2 = t^2 + t^{-2}, i.e. the map is conjugate to t -> t^2.
# For F(t) = t^n f(t + t^{-1}), the condition f(x) | f(x^2-2) becomes F(t) | F(t^2).
# This forces F to be a product of cyclotomic polynomials: F = ∏ Φ_d(t)^{e_d},
# with the divisibility equivalent to e_{2k} ≤ e_k for all k, and reciprocity imposes e_1 even.
# Degree constraint: deg F = ∑_d e_d φ(d) = 2n.
#
# The choices factor by dyadic chains rooted at odd m:
#   chain(m): d_s = 2^s m  (s ≥ 0),  weight w_s = φ(d_s).
# With nonincreasing exponents e_s (e_{s+1} ≤ e_s), the GF per chain is
#   ∏_{t≥0} 1 / (1 - q^{W_t}), where W_t = ∑_{j=0}^t w_j.
# For odd m, W_t = φ(m)·2^t (since φ(2^0)=1, φ(2^r)=2^{r-1} for r≥1).
# The special chain m=1 also needs e_1 even, i.e. parity projection:
#   (1/2) * ( ∏_{t≥0} 1/(1 - q^{2^t}) + ∏_{t≥0} 1/(1 + q^{2^t}) ).
#
# Combine all odd m≥3 by collapsing into a single Euler product:
#   ∏_{odd m≥3} ∏_{t≥0} (1 - q^{φ(m)·2^t})^{-1}
#   = ∏_{k≥1} (1 - q^k)^(-A_k),
#   where A_k = sum_{s=0..v2(k)} #{odd m≥3 : φ(m) = k / 2^s}.
# Let b[t] = #{odd m≥1 : φ(m) = t}. We exclude m=1 by skipping t=1.
# IMPORTANT: when forming A_k, halve k only while divisible by 2 (no flooring).
#
# We compute: G_odd(q) = ∏_k (1 - q^k)^(-A_k) via log/exp of formal series (NTT).
# Then multiply by the m=1 parity factor, and read [q^{2n}].
#
# Verified: S(2)=6, S(5)=58, S(20)=122087.

import sys
sys.setrecursionlimit(1_000_000)

MOD = 998244353
PRIMITIVE_ROOT = 3

############################
# Modular / NTT utilities
############################

def modinv(x: int) -> int:
    return pow(x, MOD - 2, MOD)

def ceil_pow2(n: int) -> int:
    p = 1
    while p < n:
        p <<= 1
    return p

def ntt(a, invert=False):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = modinv(wlen)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = modinv(n)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b, need_len=None):
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return []
    n = la + lb - 1
    size = ceil_pow2(n)
    fa = a[:] + [0] * (size - la)
    fb = b[:] + [0] * (size - lb)
    ntt(fa, False)
    ntt(fb, False)
    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    if need_len is None or need_len > n:
        need_len = n
    return fa[:need_len]

def poly_mul(a, b, n=None):
    c = convolution(a, b, None if n is None else n)
    if n is not None and len(c) > n:
        c = c[:n]
    return c

def poly_derivative(a):
    n = len(a)
    if n <= 1:
        return [0]
    res = [0] * (n - 1)
    for i in range(1, n):
        res[i - 1] = a[i] * i % MOD
    return res

def poly_integral(a, inv_ints):
    n = len(a)
    res = [0] * (n + 1)
    for i in range(n):
        res[i + 1] = a[i] * inv_ints[i + 1] % MOD
    return res

def poly_inv(a, n):
    # a[0] != 0
    b = [modinv(a[0])]
    m = 1
    while m < n:
        m2 = min(n, m << 1)
        a_slice = a[:m2]
        ab = poly_mul(a_slice, b, m2)
        s = [0] * m2
        s[0] = (2 - ab[0]) % MOD
        for i in range(1, m2):
            s[i] = (-ab[i]) % MOD
        b = poly_mul(b, s, m2)
        m = m2
    return b[:n]

def poly_log(a, n, inv_ints):
    # a[0] == 1
    da = poly_derivative(a)
    inv_a = poly_inv(a, n)
    mult = poly_mul(da, inv_a, max(1, n - 1))
    res = poly_integral(mult, inv_ints)
    if len(res) < n:
        res += [0] * (n - len(res))
    return res[:n]

def poly_exp(f, n, inv_ints):
    # f[0] == 0
    g = [1]
    m = 1
    while m < n:
        m2 = min(n, m << 1)
        lg = poly_log(g[:m2] + [0] * (m2 - len(g[:m2])), m2, inv_ints)
        delta = (f[:m2] + [0] * (m2 - len(f)))[:m2]
        for i in range(m2):
            delta[i] = (delta[i] - (lg[i] if i < len(lg) else 0)) % MOD
        delta[0] = (delta[0] + 1) % MOD
        g = poly_mul(g, delta, m2)
        m = m2
    return g[:n]

############################
# Count odd m with phi(m) ≤ N without scanning m
############################

def primes_upto(n):
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[0:2] = b'\x00\x00'
    import math
    for p in range(2, int(math.isqrt(n)) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n + 1:step] = b'\x00' * (((n - start) // step) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

def count_phi_odd_preimages(N):
    """
    b[t] = #{odd m ≥ 1 : φ(m) = t}, for 1 ≤ t ≤ N.
    Uses multiplicativity: φ(m) = ∏ (p-1)p^{a-1} over odd primes p.
    Enumerate products of these factors by DFS.
    """
    ps = [p for p in primes_upto(N + 1) if p != 2]
    fac_lists = []
    for p in ps:
        li = []
        f = p - 1
        while f <= N:
            li.append(f)
            if f > N // p:
                break
            f *= p
        if li:
            fac_lists.append(li)
    b = [0] * (N + 1)
    PL = len(fac_lists)

    def dfs(idx, prod):
        b[prod] += 1
        for j in range(idx, PL):
            for f in fac_lists[j]:
                if prod > N // f:
                    break
                dfs(j + 1, prod * f)

    dfs(0, 1)
    return b  # includes m=1 at t=1

############################
# Build A_k correctly (halve only while divisible by 2)
############################

def build_A_from_b(b, N):
    A = [0] * (N + 1)
    for k in range(1, N + 1):
        u = k
        while True:
            if u >= 2:
                A[k] += b[u]
            else:
                break
            if u & 1:  # stop when u is odd
                break
            u >>= 1
    return A

############################
# Log-series and exp to get ∏ (1 - q^k)^(-A_k)
############################

def build_log_series(A, N, inv_ints):
    # C[m] = (1/m) * Σ_{d|m} d A_d
    C = [0] * (N + 1)
    for d in range(1, N + 1):
        ad = A[d]
        if ad == 0:
            continue
        v = ad * d % MOD
        for m in range(d, N + 1, d):
            C[m] = (C[m] + v * inv_ints[m]) % MOD
    return C

############################
# Parity factor for the m=1 chain
############################

def parity_factor(N):
    """
    (1/2) * ( ∏_{t≥0} (1 - q^{2^t})^{-1} + ∏_{t≥0} (1 + q^{2^t})^{-1} )
    computed to degree N using residue-class DP per step.
    """
    dp_plus = [0] * (N + 1)   # for 1/(1 - x^w)
    dp_plus[0] = 1
    dp_minus = [0] * (N + 1)  # for 1/(1 + x^w)
    dp_minus[0] = 1
    inv2 = (MOD + 1) // 2
    w = 1
    while w <= N:
        # multiply by 1/(1 - x^w): prefix sums along residue classes mod w
        for r in range(w):
            limit = (N - r) // w
            s = 0
            pos = r
            for _ in range(limit + 1):
                s = (s + dp_plus[pos]) % MOD
                dp_plus[pos] = s
                pos += w
        # multiply by 1/(1 + x^w): alternating prefix sums
        for r in range(w):
            limit = (N - r) // w
            s = 0
            pos = r
            for _ in range(limit + 1):
                s = (dp_minus[pos] - s) % MOD  # s_j = a_j - s_{j-1}
                dp_minus[pos] = s
                pos += w
        if w > N // 2:
            break
        w <<= 1
    return [(dp_plus[i] + dp_minus[i]) * inv2 % MOD for i in range(N + 1)]

############################
# Main solver
############################

def S(n: int) -> int:
    N = 2 * n
    # inverses 1..N for integration / log-series
    inv_ints = [0] * (N + 1)
    inv_ints[1] = 1
    for i in range(2, N + 1):
        inv_ints[i] = MOD - (MOD // i) * inv_ints[MOD % i] % MOD

    # counts of odd m with φ(m) ≤ N
    b = count_phi_odd_preimages(N)  # includes m=1 at t=1

    # exponents for ∏_{odd m≥3} ∏_{t≥0} (1 - q^{φ(m)·2^t})^{-1} == ∏_k (1 - q^k)^(-A_k)
    # skip t=1 implicitly by only accumulating for u≥2 during halving
    A = build_A_from_b(b, N)

    # Euler-transform: F(q) = ∏ (1 - q^k)^(-A_k) = exp( Σ_{m≥1} (1/m) Σ_{d|m} d A_d q^m )
    C = build_log_series(A, N, inv_ints)
    C[0] = 0
    G_odd = poly_exp(C, N + 1, inv_ints)

    # multiply by the m=1 parity factor
    B_even = parity_factor(N)
    final = poly_mul(G_odd, B_even, n=N + 1)
    return final[N] % MOD

def main():
    # quick self-checks
    checks = {2: 6, 5: 58, 20: 122087}
    for t, want in checks.items():
        got = S(t)
        if got != want:
            print(f"[check failed] S({t}) = {got}, expected {want}")
            sys.exit(1)
    # final answer
    print(S(10_000))

if __name__ == "__main__":
    main()