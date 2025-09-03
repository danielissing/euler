#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import permutations

# ---------- core permutation ops ----------
def compose(p, q):
    # (p ∘ q)(i) = p(q(i)), one-line tuples 1..n
    return tuple(p[q[i]-1] for i in range(len(p)))

def perm_pow(p, k):
    # fast exponentiation in S_n
    res = tuple(range(1, len(p)+1))
    base = p
    while k:
        if k & 1:
            res = compose(base, res)
        base = compose(base, base)
        k >>= 1
    return res

# ---------- rank via Lehmer digits ----------
def rank_lex_one_line(p):
    n = len(p)
    used = [False]*(n+1)
    fact = [1]*(n+1)
    for i in range(1, n+1):
        fact[i] = fact[i-1]*i
    rank = 1
    for i, x in enumerate(p, start=1):
        c = 0
        for v in range(1, x):
            if not used[v]:
                c += 1
        rank += c * fact[n-i]
        used[x] = True
    return rank

# ---------- exact Q(n) by definition (works for n <= 7 quickly) ----------
def Q_bruteforce(n):
    perms = list(permutations(range(1, n+1)))  # lex order
    N = len(perms)
    # ranks in O(1) by index in itertools (already lex)
    rank = {p: i+1 for i, p in enumerate(perms)}
    total = 0
    for p in perms:
        for i in range(1, N+1):
            total += rank[perm_pow(p, i)]
    return total

if __name__ == "__main__":
    for n in [2, 3, 4, 5, 6]:
        print(f"Q({n}) =", Q_bruteforce(n))
