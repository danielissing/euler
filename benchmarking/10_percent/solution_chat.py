from math import factorial

def S(k: int) -> int:
    """
    Compute S(k) = sum over all k-digit numbers n of T(n),
    where T(n) is the number of strictly larger digit-permutations of n
    (no leading zeros allowed).

    Uses the identity:
        S(k) = sum_over_multisets C(P, 2)
    with
        P = ((k-1)! * (k - c0)) / (prod_d c_d!)
    where c0 is the count of zeros in the multiset (and sum c_d = k).
    """
    fact = [1] * (k + 1)
    for i in range(2, k + 1):
        fact[i] = fact[i - 1] * i

    total = 0
    k_1_fact = fact[k - 1]

    # Let s = k - c0 be the number of nonzero digits. s >= 1.
    # For each s, enumerate compositions of s into 9 parts (c1..c9).
    for s in range(1, k + 1):
        c0 = k - s
        denom0 = fact[c0]

        # Recursively assign counts for digits 1..8; c9 is determined at the leaf.
        def rec(pos: int, rem: int, denom_prod: int) -> None:
            nonlocal total
            if pos == 8:  # digits 1..8 assigned; digit 9 gets 'rem'
                denom_all_nonzero = denom_prod * fact[rem]
                denom_total = denom0 * denom_all_nonzero
                P = (k_1_fact * s) // denom_total  # always integer
                total += P * (P - 1) // 2
                return
            for v in range(rem + 1):
                rec(pos + 1, rem - v, denom_prod * fact[v])

        rec(0, s, 1)

    return total

if __name__ == "__main__":
    # Compute and print S(12)
    print(S(12))
