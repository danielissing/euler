#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Project Euler 889 – Rational Blancmange
# Final fast solver: works for huge k,t and r=62.
# Standard library only.

from math import comb

MOD = 1_000_062_031

def fast_F_mod(k: int, t: int, r: int, MOD: int = MOD) -> int:
    """
    Compute F(k,t,r) mod MOD for q=2^k+1, p=(2^t+1)^r, with p<q
    and t large enough so that bit-blocks for different j don't overlap
    (true for r=62 and given t).

    Uses the identity:
      F = q*(2u + S2) + p*2^k*S3  (mod MOD),
    where u = p-1, q = 2^k+1, and
      S3 = k - 2 * sum_j popcount(C(r,j)),
      S2 = sum over each 1-bit at position ell of (-ell + 2*cnt_so_far) * 2^ell (mod MOD).
    """
    # Precompute all one-bits 'ell' = t*alpha + s for coefficients C(r,alpha)
    bit_positions = []  # increasing absolute exponents ell where u has a 1-bit
    pop_u = 0
    for alpha in range(1, r + 1):
        c = comb(r, alpha)
        s = 0
        cc = c
        while cc:
            if cc & 1:
                bit_positions.append(t * alpha + s)
                pop_u += 1
            cc >>= 1
            s += 1
    bit_positions.sort()

    # S3 = k - 2 * popcount(u)
    S3_mod = ( (k % MOD) - (2 * pop_u) ) % MOD

    # S2 = -sum ell*2^ell + 2*sum (cnt_so_far)*2^ell, iterating ell increasing
    S_A_mod = 0
    S_B_mod = 0
    cnt = 0
    for ell in bit_positions:
        pow2_ell = pow(2, ell, MOD)
        S_A_mod = (S_A_mod + (ell % MOD) * pow2_ell) % MOD
        S_B_mod = (S_B_mod + cnt * pow2_ell) % MOD
        cnt += 1
    S2_mod = ( - S_A_mod + 2 * S_B_mod ) % MOD

    # p mod MOD and 2^k mod MOD
    base = (pow(2, t, MOD) + 1) % MOD
    p_mod = pow(base, r, MOD)
    u_mod = (p_mod - 1) % MOD
    two_k = pow(2, k, MOD)
    q_mod = (two_k + 1) % MOD

    term1 = (q_mod * (( (2 * u_mod) % MOD + S2_mod ) % MOD)) % MOD
    term2 = ((p_mod * two_k) % MOD) * S3_mod % MOD
    return (term1 + term2) % MOD


# ---------- sanity tests (small) ----------
def brute_F_small(k: int, t: int, r: int, MOD: int = None) -> int:
    """O(k) reference for small k, to validate formulas."""
    q = (1 << k) + 1
    p = pow((1 << t) + 1, r)  # actual integer (here we keep p<q in tests)
    acc = 0
    for n in range(k):
        rn = (p << n) % q
        dn = rn if rn <= q - rn else q - rn
        term = dn * (1 << (k - n))
        acc += term
    return acc if MOD is None else acc % MOD


if __name__ == "__main__":
    # Examples from the statement
    assert brute_F_small(3, 1, 1) == 42
    assert brute_F_small(13, 3, 3) == 23_093_880
    # The modular check in the statement:
    assert fast_F_mod(103, 13, 6, MOD) == 878_922_518

    # Final query:
    k = 10**18 + 31
    t = 10**14 + 31
    r = 62
    ans = fast_F_mod(k, t, r, MOD)
    print(ans)  # <-- prints the final answer modulo 1_000_062_031
