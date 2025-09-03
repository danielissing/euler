# Project Euler — Pisano-period product
# P(1_000_000) mod 1_234_567_891

MOD = 1_234_567_891
N = 1_000_000

def solve(n: int, mod: int) -> int:
    """
    Uses the identity:
      For p = 2t:
        M(p) = { L_t  if t is odd
               { F_t  if t is even
      For odd p: M(3)=2 and M(p)=1 for p≠3.

    Therefore:
      P(n) = 2 * ∏_{t=1}^{⌊n/2⌋} ( L_t if t odd else F_t )   (mod MOD)
    """
    T = n // 2

    # Fibonacci: F_0=0, F_1=1
    F_prev, F_curr = 0, 1
    # Lucas: L_0=2, L_1=1
    L_prev, L_curr = 2, 1

    ans = 1
    if n >= 3:                 # account for M(3)=2
        ans = (ans * 2) % mod

    # Iterate t = 1..T, multiplying the required term each time
    for t in range(1, T + 1):
        if t & 1:              # t odd -> use L_t
            ans = (ans * L_curr) % mod
        else:                  # t even -> use F_t
            ans = (ans * F_curr) % mod

        # Step the recurrences modulo mod
        F_prev, F_curr = F_curr, (F_prev + F_curr) % mod
        L_prev, L_curr = L_curr, (L_prev + L_curr) % mod

    return ans

if __name__ == "__main__":
    # quick sanity check from the prompt: P(10)=264
    # (uncomment to verify)
    # print("P(10) =", solve(10, MOD))  # -> 264

    print(solve(N, MOD))
