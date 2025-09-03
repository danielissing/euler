# Computes G(10^7) modulo 1_000_000_007 for Project Euler "beautiful graphs".
# Core facts used:
#   - Vertices partition into ordered blocks; between blocks all edges are RB with red forward.
#   - Inside a block only green/brown edges appear, with no monochromatic triangle.
#   - Therefore block sizes are ≤5 and the counts inside a block are:
#       H(1)=1, H(2)=2, H(3)=6, H(4)=18, H(5)=12.
#   - Let F(n)=G(n)/n!, then:
#       F(n)=F(n-1)+F(n-2)+F(n-3)+(3/4)F(n-4)+(1/10)F(n-5), F(0)=1.
#   - G(n)=n! * F(n) mod MOD.

MOD = 1_000_000_007

def solve(N: int) -> int:
    inv4 = pow(4, MOD - 2, MOD)
    inv10 = pow(10, MOD - 2, MOD)
    a4 = (3 * inv4) % MOD       # 3/4 mod MOD
    a5 = inv10                  # 1/10 mod MOD

    # Rolling values for F(n-5),...,F(n-1). Base: F(0)=1, earlier = 0.
    Fm5 = 0
    Fm4 = 0
    Fm3 = 0
    Fm2 = 0
    Fm1 = 1

    fact = 1
    F = 1  # current F(n)

    for n in range(1, N + 1):
        # F(n) = F(n-1)+F(n-2)+F(n-3)+(3/4)F(n-4)+(1/10)F(n-5)
        F = (Fm1 + Fm2 + Fm3 + (a4 * Fm4 + a5 * Fm5) % MOD) % MOD
        # Shift window
        Fm5, Fm4, Fm3, Fm2, Fm1 = Fm4, Fm3, Fm2, Fm1, F
        # Update n!
        fact = (fact * n) % MOD

    return (F * fact) % MOD

if __name__ == "__main__":
    N = 10_000_000
    ans = solve(N)
    print(ans)
