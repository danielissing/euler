# Overview [not reviewed yet]

**Problem link:** [Project Euler Problem
827](https://projecteuler.net/problem=827)

------------------------------------------------------------------------

## 1. Problem statement

Define $Q(n)$ as the smallest number that appears in **exactly $n$**
Pythagorean triples $(a,b,c)$ with $a < b < c$.

Examples: - $Q(5) = 15$, since $15$ is the smallest number that shows up
in 5 different triples. - $Q(10) = 48$. - $Q(10^3) = 8064000$.

**Task:** Compute

$$
\sum_{k=1}^{18} Q(10^k) \pmod{409120391}.
$$

------------------------------------------------------------------------

## 2. High-level solution idea

Instead of brute-forcing triples, we exploit number theory formulas for
how often a number $N$ can appear in a primitive or scaled Pythagorean
triple. The problem reduces to solving a **Diophantine factorization
condition** and choosing the **smallest integer $N$** consistent with
it.

Steps: 1. Derive a formula for $f(N)$, the count of triples containing
$N$. 2. Show that $f(N)$ depends only on prime exponents of $N$ split by
residue class mod 4. 3. For target $n$, solve a multiplicative factor
equation, and among all solutions construct the smallest integer $N$. 4.
Sum $Q(10^k)$ for $k=1,\dots,18$.

------------------------------------------------------------------------

## 3. The math behind the solution

-   **Triple parametrization:** Every primitive triple is $$
    (m^2-n^2,\, 2mn,\, m^2+n^2), \quad m>n, \; \gcd(m,n)=1, \; m-n \text{ odd}.
    $$

-   **Counting appearances of $N$:**

    -   If $N$ is a leg: $$
        L(N) =
        \begin{cases}
          \tfrac{\tau(N^2)-1}{2}, & N \text{ odd}, \\[6pt]
          \tfrac{\tau(N^2/4)-1}{2}, & N \text{ even},
        \end{cases}
        $$ where $\tau$ is the divisor-counting function.
    -   If $N$ is a hypotenuse: $$
        C(N) = \tfrac{1}{2}\!\left(\!\prod_{p\equiv 1\pmod{4}} (2\alpha_p+1) - 1\!\right),
        $$ where
        $N=2^a \prod_{p\equiv 1(4)} p^{\alpha_p} \prod_{q\equiv 3(4)} q^{\beta_q}$.

-   **Unification:** With

    -   $U=\prod_{q\equiv 3(4)} (2\beta_q+1)$,
    -   $V=\prod_{p\equiv 1(4)} (2\alpha_p+1)$,
    -   $M=1$ if $a=0$, else $M=2a-1$ (always odd),

    we obtain the key identity: $$
    f(N)+1 = \frac{V \, (MU+1)}{2}.
    $$

-   **Target equation:** For given $n$, $$
    V(MU+1) = 2(n+1).
    $$

-   **Constructing $Q(n)$:**

    -   Choose an odd divisor $V$ of $n+1$.
    -   Set $W = \tfrac{2(n+1)}{V}$, then $MU = W-1$.
    -   Factor $MU$ into $M\cdot U$ with $M$ odd.
    -   Build the minimal $N$ from:
        -   exponents $\alpha$ from factorization of $V$ (using primes
            $1 \pmod 4$),
        -   exponents $\beta$ from factorization of $U$ (using primes
            $3 \pmod 4$),
        -   power of 2 from $M$.

------------------------------------------------------------------------

## 4. Techniques used to increase algorithmic efficiency

-   **Closed-form counting:** Avoid generating triples by hand. Use
    divisor/arithmetic formulas for appearances.
-   **Factorization reduction:** Only need to factor numbers of form
    $10^k+1$ and divisors thereof (up to $k=18$).
-   **Pollard's Rho + Miller--Rabin:** Efficient 64-bit integer
    factorization.
-   **Search pruning:** Only consider odd divisor splits $V, M, U$. This
    keeps search space small.
-   **Minimal number construction:** Assign larger exponents to smaller
    primes (by congruence class) to guarantee minimal $N$.
-   **Logarithmic comparison:** Compare candidates by $\log N$ instead
    of building full big integers; compute final result modulo
    $409120391$ with modular exponentiation.
