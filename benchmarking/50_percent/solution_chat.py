# Python 3.13+; standard library only
# Computes sum_{k=1..18} Q(10^k) mod 409120391

import math, random
from functools import lru_cache

MOD = 409120391

# ---------- Miller-Rabin (deterministic for 64-bit) ----------
def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small:
        if n % p == 0:
            return n == p
    # n-1 = d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # bases suffice for n < 2^64
    for a in [2,3,5,7,11,13,17]:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = (x * x) % n
            if x == n-1:
                break
        else:
            return False
    return True

# ---------- Pollard Rho factoring ----------
def _pollard_rho(n: int) -> int:
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    if n % 5 == 0: return 5
    while True:
        c = random.randrange(1, n-1)
        f = lambda x: (pow(x, 2, n) + c) % n
        x = random.randrange(2, n-1)
        y = x
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d

def _factor(n: int, out: dict):
    if n == 1:
        return
    if is_probable_prime(n):
        out[n] = out.get(n, 0) + 1
        return
    d = _pollard_rho(n)
    _factor(d, out)
    _factor(n // d, out)

def factorize(n: int) -> dict:
    res = {}
    _factor(n, res)
    return res

def divisors_from_factors(f: dict) -> list[int]:
    divs = [1]
    for p, e in f.items():
        cur = []
        pe = 1
        for _ in range(e+1):
            for d in divs:
                cur.append(d * pe)
            pe *= p
        divs = cur
    return divs

# ---------- small primes by sieve; split by mod 4 ----------
def primes_upto(n: int) -> list[int]:
    sieve = bytearray(b'\x01') * (n+1)
    sieve[0:2] = b'\x00\x00'
    for p in range(2, int(n**0.5)+1):
        if sieve[p]:
            step = p
            start = p*p
            sieve[start:n+1:step] = b'\x00' * (((n - start)//step) + 1)
    return [i for i in range(2, n+1) if sieve[i]]

_primes = primes_upto(10000)  # plenty for our exponent counts
P1 = [p for p in _primes if p % 4 == 1]  # 5, 13, 17, ...
P3 = [p for p in _primes if p % 4 == 3]  # 3, 7, 11, ...

LOG_P1 = [math.log(p) for p in P1]
LOG_P3 = [math.log(p) for p in P3]
LOG2 = math.log(2.0)

# ---------- caches ----------
div_cache: dict[int, list[int]] = {}
def divisors_cached(n: int) -> list[int]:
    """All divisors of n (sorted)."""
    if n in div_cache:
        return div_cache[n]
    f = factorize(n)
    divs = sorted(divisors_from_factors(f))
    div_cache[n] = divs
    return divs

@lru_cache(maxsize=None)
def _min_value_from_X(X: int, which: int) -> tuple[float, tuple[int, ...]]:
    """
    Minimal log-value and exponents (tuple) for product prod p_i^{gamma_i}
    subject to \prod (2*gamma_i + 1) = X.
    'which' = 1 for P1 primes, =3 for P3 primes.
    """
    if X == 1:
        return (0.0, ())
    logs = LOG_P1 if which == 1 else LOG_P3
    divs = divisors_cached(X)
    idx_of = {d: i for i, d in enumerate(divs)}

    @lru_cache(maxsize=None)
    def dfs(rem: int, idx: int, last_idx: int) -> tuple[float, tuple[int, ...]]:
        if rem == 1:
            return (0.0, ())
        if idx >= len(logs):
            return (float('inf'), ())
        best_log = float('inf'); best_tuple: tuple[int, ...] = ()
        last_d = divs[last_idx]
        # try divisors t of rem with 3 <= t <= last_d, descending helps a bit
        for t in reversed(divs):
            if t > last_d or t < 3: continue
            if rem % t != 0: continue
            alpha = (t - 1) // 2
            cur = alpha * logs[idx]
            sub_log, sub_tuple = dfs(rem // t, idx + 1, idx_of[t])
            val = cur + sub_log
            if val < best_log:
                best_log = val
                best_tuple = (alpha,) + sub_tuple
        return (best_log, best_tuple)

    return dfs(X, 0, idx_of[X])

def min_value_from_X(X: int, which: int) -> tuple[float, tuple[int, ...]]:
    """Wrapper to make the cache signature hashable."""
    return _min_value_from_X(X, which)

# ---------- core: Q(10^k) ----------
def Q_pow10(k: int) -> int:
    random.seed(0xC0FFEE + k)  # stabilize Pollard-Rho randomness
    R = 10**k + 1             # odd
    # Enumerate odd divisors D of R (since V = R / D, MU+1 = 2D)
    divs_R = divisors_cached(R)
    best_log = float('inf')
    best_a = 0
    best_ev: tuple[int, ...] = ()
    best_eu: tuple[int, ...] = ()

    for D in divs_R:
        if D % 2 == 0:  # R is odd, so odd divisors only; harmless check
            continue
        V = R // D                # odd
        W = 2 * D                 # even
        S = W - 1                 # MU = S, odd
        # get minimal build for V on 1 mod 4 primes
        logV, ev = min_value_from_X(V, which=1)
        # enumerate M | S (odd divisors)
        divs_S = divisors_cached(S)  # S is odd
        for M in divs_S:
            if M % 2 == 0:  # S odd => divisors odd; harmless check
                continue
            a = 0 if M == 1 else (M + 1) // 2
            U = S // M
            logU, eu = min_value_from_X(U, which=3)
            logN = a * LOG2 + logV + logU
            if logN < best_log - 1e-12:
                best_log = logN
                best_a, best_ev, best_eu = a, ev, eu

    # Reconstruct N modulo MOD from exponents
    ans = pow(2, best_a, MOD)
    for i, alpha in enumerate(best_ev):
        ans = (ans * pow(P1[i], alpha, MOD)) % MOD
    for i, beta in enumerate(best_eu):
        ans = (ans * pow(P3[i], beta, MOD)) % MOD
    return ans

def main():
    total = 0
    for k in range(1, 19):
        total = (total + Q_pow10(k)) % MOD
    print(total)

if __name__ == "__main__":
    main()
