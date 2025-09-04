# Project Euler 791: Avergae and variance

from math import isqrt

MOD = 433_494_437

def sqsum(n: int) -> int:
    """Sum_{k=1..n} k^2."""
    if n <= 0:
        return 0
    return n*(n+1)*(2*n+1)//6

def sumsq_interval(t0: int, s: int) -> int:
    """Sum_{i=0..s-1} (t0+i)^2 (exact)."""
    return s*t0*t0 + t0*s*(s-1) + (s*(s-1)*(2*s-1))//6

def tmax_for(rhs: int) -> int:
    """Largest t with t^2 + t <= rhs (rhs>=0)."""
    return (isqrt(1 + 4*rhs) - 1) // 2

def solve_S(n: int, mod: int = MOD) -> int:
    ans = 0
    two = 2 % mod
    Amax = tmax_for(2*n)

    for A in range(Amax + 1):
        AA = A*A
        # Overall t-range at this A: A <= t <= t_hi
        rhs_t = 2*n - (AA + A)
        if rhs_t < 0:
            break
        t_lo = A
        t_hi = tmax_for(rhs_t)
        if t_hi < t_lo:
            continue

        # ---------- Range 1: both sides saturated (U>=A, R>=A) ----------
        t_both = tmax_for(2*n - 2*AA - 2*A)  # T >= A^2 + A
        if t_both > t_hi: t_both = t_hi
        if t_both >= t_lo:
            k = t_both - t_lo + 1                       # number of t
            N = 2*A + 1                                  # 1 + A + A
            SG2 = 2 * sqsum(A)                           # sum G^2 on both sides
            s1 = sumsq_interval(t_lo, k)                 # sum t^2 over the block
            part = ( two * ( ((AA % mod)*(k % mod) + (s1 % mod)) % mod ) * (N % mod)
                     + two * ((SG2 % mod)*(k % mod)) ) % mod
            ans += part
            if ans >= mod: ans -= mod
            t_cur = t_both + 1
        else:
            t_cur = t_lo

        # ---------- Range 2: positive saturated only (U>=A, R=A-1) ----------
        t_pos = tmax_for(2*n - 2*AA)                     # T >= A^2 - A
        if t_pos > t_hi: t_pos = t_hi
        if t_cur <= t_pos:
            k = t_pos - t_cur + 1
            N = 2*A                                      # 1 + A + (A-1)
            SG2 = sqsum(A) + sqsum(A-1)
            s1 = sumsq_interval(t_cur, k)
            part = ( two * ( ((AA % mod)*(k % mod) + (s1 % mod)) % mod ) * (N % mod)
                     + two * ((SG2 % mod)*(k % mod)) ) % mod
            ans += part
            if ans >= mod: ans -= mod
            t_cur = t_pos + 1

        # ---------- Range 3: unsaturated tail (U<A, R=U-1), block stepping ----------
        while t_cur <= t_hi:
            # T(A,t) and U from T
            T = 2*n - (AA + t_cur*t_cur + A + t_cur)
            U = (isqrt(1 + 4*T) + 1) // 2               # floor((1+sqrt(1+4T))/2)
            N = 2*U                                      # 1 + U + (U-1)
            SG2 = sqsum(U) + sqsum(U-1)

            # Max steps s (>=1) until U would drop (i.e., T < U(U-1)).
            # T_{t+s} = T - s*(2*t_cur + 1) - s*(s-1)
            rhs = T - U*(U-1)
            s_max = isqrt(t_cur*t_cur + rhs) - t_cur
            if s_max < 1:
                s_max = 1
            if t_cur + s_max - 1 > t_hi:
                s_max = t_hi - t_cur + 1

            s1 = sumsq_interval(t_cur, s_max)
            part = ( two * ( ((AA % mod)*(s_max % mod) + (s1 % mod)) % mod ) * (N % mod)
                     + two * ((SG2 % mod)*(s_max % mod)) ) % mod
            ans += part
            if ans >= mod: ans -= mod
            t_cur += s_max

        # ---------- a >= 1 corrections (remove a=0 cases) ----------
        # (A,t,G) = (0,1,0): subtract 2*(A^2 + t^2 + 0) = 2
        if A == 0 and t_lo <= 1 <= t_hi:
            ans = (ans - 2) % mod
        # (A,t,G) = (1,1,0) and (1,1,1): subtract 2*(A^2 + t^2 + 0) + 2*(A^2 + t^2 + 1) = 10
        if A == 1 and t_lo <= 1 <= t_hi:
            ans = (ans - 10) % mod

    return ans % mod

if __name__ == "__main__":
    # Sanity checks from the statement
    assert solve_S(5) == 48
    assert solve_S(10**3) == 37_048_340
    # Final answer
    print(solve_S(10**8))
