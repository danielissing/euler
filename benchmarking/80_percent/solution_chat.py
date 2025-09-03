# Computes S(100) for the "absolute neighbour differences on a circle" problem
# using the Rule-90 / finite-field approach described above.
# Standard library only.

import math
from functools import reduce

# ---------- basic number theory ----------

def phi(n):
    res = n
    p = 2
    t = n
    while p * p <= t:
        if t % p == 0:
            while t % p == 0:
                t //= p
            res -= res // p
        p += 1
    if t > 1:
        res -= res // t
    return res

def prime_factors_small(n):
    """factor n into primes (n <= ~1e7 here), returns dict p->exp (used for small d)"""
    res = {}
    p = 2
    t = n
    while p * p <= t:
        if t % p == 0:
            cnt = 0
            while t % p == 0:
                t //= p
                cnt += 1
            res[p] = cnt
        p += 1
    if t > 1:
        res[t] = 1
    return res

def multiplicative_order_mod(a, n):
    """ord_n(a) for gcd(a,n)=1"""
    if math.gcd(a, n) != 1:
        return 0
    ph = phi(n)
    o = ph
    for p in list(prime_factors_small(ph).keys()):
        while o % p == 0 and pow(a, o // p, n) == 1:
            o //= p
    return o

# ---------- bit-polynomial over GF(2) ----------

def pdeg(p):  # degree
    return p.bit_length() - 1

def padd(a, b):  # add over GF(2)
    return a ^ b

def pmul(a, b):  # multiply polynomials over GF(2), no reduction
    res = 0
    x = a
    y = b
    while y:
        if y & 1:
            res ^= x
        y >>= 1
        x <<= 1
    return res

def pmod(a, mod):  # reduce modulo monic mod
    dm = pdeg(mod)
    x = a
    while pdeg(x) >= dm:
        x ^= (mod << (pdeg(x) - dm))
    return x

def pmul_mod(a, b, mod):
    return pmod(pmul(a, b), mod)

def ppow_mod(base, exp, mod):
    r = 1
    b = base
    e = exp
    while e:
        if e & 1:
            r = pmul_mod(r, b, mod)
        b = pmul_mod(b, b, mod)
        e >>= 1
    return r

def pgcd(a, b):
    x, y = a, b
    while y:
        x, y = y, pmod(x, y)
    return x

def psquare_mod(a, mod):
    # (sum a_i x^i)^2 = sum a_i x^(2i) over GF(2)
    res = 0
    i = 0
    x = a
    while x:
        if x & 1:
            res ^= (1 << (2 * i))
        x >>= 1
        i += 1
    return pmod(res, mod)

def is_irreducible(f, m):
    # Rabin test for irreducibility over GF(2)
    x = 0b10
    # x^(2^m) == x mod f
    z = x
    for _ in range(m):
        z = psquare_mod(z, f)
    if z != x:
        return False
    # For each prime q|m: gcd(x^(2^(m/q)) - x, f) == 1
    temp = m
    primes = set()
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            primes.add(p)
            while temp % p == 0:
                temp //= p
        p += 1
    if temp > 1:
        primes.add(temp)
    for q in primes:
        z = x
        for _ in range(m // q):
            z = psquare_mod(z, f)
        if pgcd(f, z ^ x) != 1:
            return False
    return True

def find_irreducible(m):
    """deterministic search; try trinomials then a seeded 'random-like' search"""
    # Try trinomials x^m + x^k + 1
    for k in range(1, m):
        f = (1 << m) | (1 << k) | 1
        if is_irreducible(f, m):
            return f
    # Seeded pseudo-random tries
    seed = 1234567 + 98765 * m
    x = seed & 0x7fffffff
    tries = 2000 + 50 * m
    for _ in range(tries):
        # linear congruential generator (deterministic)
        x = (1103515245 * x + 12345) & 0x7fffffff
        # scatter ~m/2 random bits
        lower = 1
        y = x
        for _ in range(m // 2):
            y = (1103515245 * y + 54321) & 0x7fffffff
            bit = 1 + (y % (m - 1))
            lower |= (1 << bit)
        f = (1 << m) | lower
        if is_irreducible(f, m):
            return f
    # As a last resort, limited sequential scan of small space
    limit = 1 << min(m, 24)
    base = (1 << m)
    for lower in range(1, limit, 2):
        f = base | lower
        if is_irreducible(f, m):
            return f
    raise RuntimeError(f"Cannot find irreducible polynomial of degree {m}")

# ---------- GF(2^m) arithmetic via modulus f ----------

def gf_mul(a, b, f):
    res = 0
    x = a
    y = b
    mdeg = pdeg(f)
    top = 1 << mdeg
    while y:
        if y & 1:
            res ^= x
        y >>= 1
        x <<= 1
        if x & top:
            x ^= f
    return res

def gf_pow(a, e, f):
    r = 1
    b = a
    while e:
        if e & 1:
            r = gf_mul(r, b, f)
        b = gf_mul(b, b, f)
        e >>= 1
    return r

# ---------- factor 2^{m'} - 1 by trial division (m' <= 41 here) ----------

def sieve(n):
    s = bytearray(b"\x01") * (n + 1)
    s[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if s[p]:
            step = p
            start = p * p
            s[start:n + 1:step] = b"\x00" * (((n - start) // step) + 1)
    return [i for i, b in enumerate(s) if b]

def factor_integer(N, primes):
    res = {}
    t = N
    for p in primes:
        if p * p > t:
            break
        if t % p == 0:
            cnt = 0
            while t % p == 0:
                t //= p
                cnt += 1
            res[p] = cnt
    if t > 1:
        res[t] = res.get(t, 0) + 1
    return res

# ---------- compute orders of beta = alpha^t + alpha^{-t} for each odd d ----------

def beta_orders_for_d(d, fmods_by_m, N_fact_cache, primes):
    # m = ord_d(2)
    m = multiplicative_order_mod(2, d)
    if m == 0:
        return {1}
    if (m % 2) == 0 and pow(2, m // 2, d) == d - 1:
        mprime = m // 2
    else:
        mprime = m
    N = (1 << mprime) - 1
    if mprime not in N_fact_cache:
        N_fact_cache[mprime] = factor_integer(N, primes)
    N_primes = list(N_fact_cache[mprime].keys())

    # field GF(2^m)
    f = fmods_by_m[m]
    group_order = (1 << m) - 1
    assert group_order % d == 0
    proj = group_order // d

    # find an element alpha of exact order d: alpha = g^{(2^m - 1)/d} then adjust
    alpha = None
    d_primes = list(prime_factors_small(d).keys())
    for seed in range(1, min(512, (1 << m))):
        a = gf_pow(seed, proj, f)
        if gf_pow(a, d, f) != 1:
            continue
        ok = True
        for p in d_primes:
            if gf_pow(a, d // p, f) == 1:
                ok = False
                break
        if ok:
            alpha = a
            break
    if alpha is None:
        raise RuntimeError(f"Failed to find alpha of order {d} in GF(2^{m})")

    # loop over t coprime to d; beta_t = alpha^t + alpha^{-t}
    orders = set()
    for t in range(1, d):
        if math.gcd(t, d) != 1:
            continue
        at = gf_pow(alpha, t, f)
        inv_at = gf_pow(alpha, (d - t) % d, f)  # alpha^{d-t} = alpha^{-t}
        beta = at ^ inv_at
        if beta == 0:
            continue
        # multiplicative order of beta dividing N
        ord_beta = N
        for p in N_primes:
            while (ord_beta % p) == 0 and gf_pow(beta, ord_beta // p, f) == 1:
                ord_beta //= p
        orders.add(ord_beta)
    if not orders:
        orders.add(1)
    return orders

# ---------- assemble periods for each n ----------

def lcm(a, b):
    return a // math.gcd(a, b) * b

def lcm_closure(values):
    S = {1}
    for v in values:
        S.update({lcm(x, v) for x in S})
    return S

def compute_periods_up_to(N):
    # precompute unique m and m' values to size the sieve for factoring 2^{m'}-1
    m_values = set()
    mprime_values = set()
    for d in range(3, N + 1, 2):
        m = multiplicative_order_mod(2, d)
        if m == 0:
            continue
        m_values.add(m)
        if (m % 2) == 0 and pow(2, m // 2, d) == d - 1:
            mprime_values.add(m // 2)
        else:
            mprime_values.add(m)
    max_mprime = max(mprime_values)
    maxN = (1 << max_mprime) - 1
    primes = sieve(int(math.isqrt(maxN)) + 1)

    # field moduli per m
    fmods_by_m = {m: find_irreducible(m) for m in sorted(m_values)}
    N_fact_cache = {}

    # orders for each odd d
    Ods = {}
    for d in range(3, N + 1, 2):
        Ods[d] = beta_orders_for_d(d, fmods_by_m, N_fact_cache, primes)

    # build P(n) and union over n
    union = set()
    for n in range(3, N + 1):
        # n = 2^k * m_odd
        m_odd = n
        k = 0
        while (m_odd % 2) == 0:
            m_odd //= 2
            k += 1
        # odd part orders: union over odd d | m_odd
        odd_orders = set()
        for d in range(3, m_odd + 1, 2):
            if (m_odd % d) == 0:
                odd_orders |= Ods[d]
        odd_lcms = lcm_closure(sorted(odd_orders))
        # combine with 2-powers
        periods = {1}
        for L in odd_lcms:
            if L == 1:
                continue
            for e in range(k + 1):
                periods.add(L << e)
        if (m_odd % 3) == 0:
            for e in range(1, k + 1):
                periods.add(1 << e)
        union |= periods
    return union

if __name__ == "__main__":
    # small checks
    U6 = compute_periods_up_to(6)
    assert sum(U6) == 6  # {1,2,3}
    U30 = compute_periods_up_to(30)
    assert sum(U30) == 20381  # given in problem

    U100 = compute_periods_up_to(100)
    ans = sum(U100)
    print(f"S(100) = {ans}")
