# Overview

**Problem link:** Project Euler – Blancmange / Takagi function variant (F(k,t,r))

Explanations below follow the final fast solver described previously (bit‑dynamical / popcount method).

---

## 1. Problem statement

Recall the blancmange (Takagi) function $$T(x)=\sum_{n\ge 0}\frac{s(2^n x)}{2^n}$$ where $$s(x)$$ is the distance from $$x$$ to the nearest integer.  
For positive integers $$k,t,r$$ define
$$F(k,t,r)=(2^{2k}-1)\,T\!\left(\dfrac{(2^t+1)^r}{2^k+1}\right).$$
It is known that $$F(k,t,r)\in\mathbb{Z}$$.  

**Task:** Compute $$F(10^{18}+31,\,10^{14}+31,\,62)\pmod{1\,000\,062\,031}$$.

---

## 2. High‑level solution idea

- Set $$q=2^k+1$$ and $$p=(2^t+1)^r$$; in our instance $$p\ll q$$.  
- Consider $$x=p/q$$. Under doubling, the fractional parts $$\{2^i x\}$$ determine the terms of $$T(x)$$; only whether a term lies above or below $$\tfrac12$$ matters for the “distance to the nearest integer.”  
- For this special modulus $$q=2^k+1$$, one has $$2^k\equiv -1\pmod q$$. The first $$k$$ binary digits of $$x$$ turn out to be exactly the $$k$$‑bit binary digits of $$u:=p-1$$.  
- Because $$t\gg r$$ and $$p=(1+2^t)^r$$, the binary expansion of $$u$$ is the **disjoint union of separated blocks** (no carries between different binomial terms).  
- This lets us rewrite the full value of $$F(k,t,r)$$ using only:
  1) the **popcount** of $$u$$ (how many 1‑bits), and  
  2) a short weighted sum over the **positions** of those 1‑bits, all done modulo the required prime.  
- No iteration up to $$k\approx 10^{18}$$ and no construction of $$2^k$$ is needed.

---

## 3. The math behind the solution

Let $$x=p/q$$ with $$q=2^k+1$$, $$p=(2^t+1)^r$$, and write the binary digits of $$x$$ as $$0.b_1b_2\ldots$$.  
For the distance-to-nearest-integer pieces, define $$\operatorname{sgn}_i=+1$$ if $$\{2^i x\}\le \tfrac12$$ and $$-1$$ otherwise. Then $$\operatorname{sgn}_i=1-2b_{i+1}$$.

A key identity for $$p<q$$ is
$$\left\lfloor 2^k x\right\rfloor=\left\lfloor\frac{2^k p}{2^k+1}\right\rfloor=p-1=:u,$$
so the first $$k$$ bits $$b_1\ldots b_k$$ are exactly the $$k$$‑bit expansion of $$u$$.  
From the standard period‑compression for the blancmange at dyadic rationals and some algebra (pairing indices using $$2^k\equiv-1\pmod q$$), one obtains an exact finite formula
$$F(k,t,r)\;=\;q\bigl(2u+S_2\bigr)+p\,2^k\,S_3,$$
where
$$S_3\;=\;\sum_{i=0}^{k-1}\operatorname{sgn}_i\;=\;k-2\,\mathrm{popcount}(u),$$
and $$S_2$$ is a short weighted sum that depends only on the positions of 1‑bits of $$u$$.

Since $$p=(1+2^t)^r=\sum_{j=0}^r\binom{r}{j}2^{tj}$$ and $$t\gg r$$, the binary blocks do not overlap and hence
$$\mathrm{popcount}(u)=\sum_{j=1}^r\mathrm{popcount}\!\left(\binom{r}{j}\right).$$
Enumerate the 1‑bits of $$u$$ in increasing order. If a 1‑bit occurs at absolute position $$\ell$$ (i.e., the coefficient of $$2^\ell$$ in $$u$$ is 1), and if $$\mathrm{rank}(\ell)$$ denotes how many earlier 1‑bits have been seen, then
$$S_2\;\equiv\;\sum_{\ell}\bigl(-\ell+2\,\mathrm{rank}(\ell)\bigr)\,2^{\ell}\;\;\;\;\;\;(\bmod\ M),$$
with $$M=1{,}000{,}062{,}031$$.  
Finally, compute
$$F\;\equiv\;(2^k+1)\bigl(2(p-1)+S_2\bigr)+p\,2^k\bigl(k-2\,\mathrm{popcount}(u)\bigr)\quad(\bmod\ M),$$
using modular exponentiation for every occurrence of $$2^k$$ and $$2^{\ell}$$. Only about $$\sum_j \mathrm{popcount}\binom{62}{j}\approx 1.3\times 10^3$$ terms appear.

---

## 4. Techniques used to increase algorithmic efficiency

- **No giant integers:** never form $$2^k$$ or $$q=2^k+1$$ explicitly; compute only $$2^k\bmod M$$ and $$2^{\ell}\bmod M$$ via fast modular exponentiation.  
- **Bit‑block separation:** exploit $$t\gg r$$ so the expansion of $$(1+2^t)^r-1$$ has non‑overlapping binary blocks; this turns carries off and makes popcounts additive.  
- **Popcount and bit‑positions only:** reduce the problem to $$\mathrm{popcount}(u)$$ and a short sum over the 1‑bit positions of $$u$$; for $$r=62$$ this is only about 1–2 thousand terms.  
- **Dyadic periodicity:** use $$2^k\equiv -1\pmod q$$ to compress the infinite series for $$T(x)$$ into a finite closed form in one pass.  
- **Memory‑light:** the algorithm is $$O\!\left(\sum_j \mathrm{popcount}\binom{r}{j}\right)$$ time and constant memory aside from a small list of bit positions.
