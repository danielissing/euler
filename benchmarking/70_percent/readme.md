# Overview [not yet reviewed]

**Problem link:** [Project Euler Problem 889](https://projecteuler.net/problem=889)  

---

## 1. Problem statement

Recall the blancmange (Takagi) function 

$$
T(x)=\sum_{n\ge 0}\frac{s(2^n x)}{2^n}
$$

where $s(x)$ is the distance from $x$ to the nearest integer.  
For positive integers $k,t,r$ define

$$
F(k,t,r)=(2^{2k}-1)T\!\left(\dfrac{(2^t+1)^r}{2^k+1}\right).
$$

It is known that $F(k,t,r)\in\mathbb{Z}$.  

**Task:** Compute $F(10^{18}+31,10^{14}+31,62)\pmod{1000062031}$.

---

## 2. High‑level solution idea

- **Define the key numbers.**  
  We set up two values: one very large denominator and one smaller numerator. In our case, the numerator is tiny compared with the denominator.

- **Understand how the function is built.**  
  The function adds up contributions based on repeatedly doubling the fraction `p/q`. Each doubling step depends only on whether the fractional part lands above or below one-half. That “above or below” decision controls the term’s size.

- **Exploit the special denominator.**  
  With this particular choice of denominator, doubling it many times cycles in a very simple way: after a huge number of steps it behaves as though we flipped the sign. This means the binary digits of the numerator essentially *become* the first chunk of binary digits of the fraction. In practice, the structure of the numerator completely dictates the behavior.

- **Describe the numerator’s pattern.**  
  Because of how the numerator is defined, its binary representation splits neatly into widely separated blocks of ones. Each block comes from a different piece of the expansion, and they never interfere with one another (no “carry” between them). This makes the binary pattern especially easy to analyze.

- **Compute the result efficiently.**  
  The entire value we want boils down to just two ingredients:
  1. How many ones appear in the numerator’s binary expansion (the **popcount**).  
  2. A simple weighted sum of the positions of those ones.  

  With these two pieces, we can write down the result directly. Everything is carried out with modular arithmetic, and we never need to explicitly build the gigantic numbers like `2^k`.
---

## 3. The math behind the solution

Let $x=p/q$ with $q=2^k+1$, $p=(2^t+1)^r$, and write the binary digits of $x$ as $0.b_1b_2\ldots$.  
For the distance-to-nearest-integer pieces, define $sgn_i=+1$ if $\{2^i x\}\le \tfrac12$ and $-1$ otherwise. Then $sgn_i=1-2b_{i+1}$.

A key identity for $p<q$ is

$$
\left\lfloor 2^k x\right\rfloor=\left\lfloor\frac{2^k p}{2^k+1}\right\rfloor=p-1=:u,
$$

so the first $k$ bits $b_1\ldots b_k$ are exactly the $k$‑bit expansion of $u$.  
From the standard period‑compression for the blancmange at dyadic rationals and some algebra (pairing indices using $2^k\equiv-1\pmod q$), one obtains an exact finite formula

$$
F(k,t,r)=q\bigl(2u+S_2\bigr)+p2^kS_3,
$$

where
$S_3=\sum_{i=0}^{k-1}sgn_i=k-2\mathrm{popcount}(u),$
and $S_2$ is a short weighted sum that depends only on the positions of 1‑bits of $u$.

Since $p=(1+2^t)^r=\sum_{j=0}^r\binom{r}{j}2^{tj}$ and $t\gg r$, the binary blocks do not overlap and hence
$\mathrm{popcount}(u)=\sum_{j=1}^r\mathrm{popcount}\!\left(\binom{r}{j}\right).$
Enumerate the 1‑bits of $u$ in increasing order. If a 1‑bit occurs at absolute position $\ell$ (i.e., the coefficient of $2^\ell$ in $u$ is 1), and if $\mathrm{rank}(\ell)$ denotes how many earlier 1‑bits have been seen, then

$$
S_2\equiv\sum_{\ell}\bigl(-\ell+2\mathrm{rank}(\ell)\bigr)2^{\ell}(\bmod\ M),
$$

with $M=1{,}000{,}062{,}031$.  
Finally, compute

$$
F\equiv(2^k+1)\bigl(2(p-1)+S_2\bigr)+p2^k\bigl(k-2\mathrm{popcount}(u)\bigr)\quad(\bmod\ M),
$$

using modular exponentiation for every occurrence of $2^k$ and $2^{\ell}$. Only about $\sum_j \mathrm{popcount}\binom{62}{j}\approx 1.3\times 10^3$ terms appear.

---

## 4. Techniques used to increase algorithmic efficiency

- **No giant integers:** never form $2^k$ or $q=2^k+1$ explicitly; compute only $2^k\bmod M$ and $2^{\ell}\bmod M$ via fast modular exponentiation.  
- **Bit‑block separation:** exploit $t\gg r$ so the expansion of $(1+2^t)^r-1$ has non‑overlapping binary blocks; this turns carries off and makes popcounts additive.  
- **Popcount and bit‑positions only:** reduce the problem to $\mathrm{popcount}(u)$ and a short sum over the 1‑bit positions of $u$; for $r=62$ this is only about 1–2 thousand terms.  
- **Dyadic periodicity:** use $2^k\equiv -1\pmod q$ to compress the infinite series for $T(x)$ into a finite closed form in one pass.  
- **Memory‑light:** the algorithm is $O\!\left(\sum_j \mathrm{popcount}\binom{r}{j}\right)$ time and constant memory aside from a small list of bit positions.
