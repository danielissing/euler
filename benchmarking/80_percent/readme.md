# Overview [not reviewed yet]

**Problem link:** [Project Euler Problem 843](https://projecteuler.net/problem=843)

---

## 1. Problem statement

You are given a circle of $n\ge 3$ integers. In one synchronous step, every entry is replaced by the absolute difference of its two neighbours.  
For any initial values, the process eventually becomes periodic. Let $S(N)$ be the **sum of all distinct periods that can occur** for any circle size n with $3\le n\le N$. 

**Task:** Given that S(6)=6 and S(30)=20381, compute S(100).

---

## 2. High-level solution idea

Work **modulo 2** first: absolute difference equals XOR, so one update is exactly
$$a_i \mapsto a_{i-1}\oplus a_{i+1},$$
i.e. Rule 90 on a ring of length $n$. Over $\mathbb{F}_2$ this is a **linear map** whose odd period fully controls the long-term behaviour over the integers; when n is even, periods can get multiplied by a power of two.

Plan:
1. Model states as polynomials in the ring $\mathbb{F}_2[x]/(x^n-1)$. One step is multiplication by $L(x)=x+x^{-1}.$
2. Decompose by odd divisors d\mid n. For a root \alpha of order d we track $\beta=\alpha+\alpha^{-1}.$
   The **odd period** contributed by that component is the multiplicative order of \beta in a suitable field $\mathbb{F}_{2^{m'}}$.
3. All odd periods for a fixed n are **LCMs** of component orders. For even n, multiply by any allowed $2^e$ (bounded by the 2-adic valuation of n); some cases also allow **pure powers of two**.
4. Union the attainable periods across all $3\le n\le N$ and sum them to get $S(N)$.

---

## 3. The math behind the solution

**Linear-algebra view modulo 2.** Encode a state as

$$
A(x)=\sum_{i=0}^{n-1} a_i x^i\in \mathbb{F}_2[x]/(x^n-1),
$$

where one step is

$$
A\;\longmapsto\; L(x)\,A,\qquad L(x)=x+x^{-1}
$$

(with $x^{-1}\equiv x^{n-1})$. Factor

$$
x^n-1=\prod_{d\mid n}\Phi_d(x),
$$

and restrict to **odd** d, since parity dynamics lives in the odd part.

Fix odd $d\mid n$. Let $m=\mathrm{ord}_d(2)$ be the multiplicative order of 2 modulo d, so that $\mathbb{F}_2[x]/(\Phi_d)\cong\mathbb{F}_{2^m}$ and a primitive d-th root $\alpha$ lies in $\mathbb{F}_{2^m}$. The scalar action of one step on this component is

$$
\beta = \alpha+\alpha^{-1}.
$$

The element $\beta$ lies in the subfield of $\mathbb{F}_{2^m}$ fixed by inversion; thus the relevant field is

$$
m' = \begin{cases}
m/2, & \text{if }2^{m/2}\equiv -1\pmod d,\\
m, & \text{otherwise,}
\end{cases}
$$

and the multiplicative group has size $2^{m'}-1.$ 
Therefore the **component period** is

$$
ord(\beta)\ \mid\ 2^{m'}-1.
$$

Let $n=2^k\,n_{\text{odd}}$. Writing $\mathcal{O}(d)$ for the set of orders $ord(\beta)$ that occur as $\alpha ranges$ over elements of order $d$ and $\beta=\alpha^t+\alpha^{-t}$ with $\gcd(t,d)=1$, the attainable **odd periods** for n form the LCM-closure

$$
\mathcal{L}(n)=\text{LCM-closure}\Big(\ \bigcup_{d\mid n_{\text{odd}},\ d\text{ odd}}\mathcal{O}(d)\ \Big).
$$

Finally the full set of periods for n is

$$
\lbrace 1 \rbrace\ \cup\ \lbrace\ 2^e\,L\ :\ L\in\mathcal{L}(n),\ L>1,\ 0\le e\le k\ \rbrace\ \cup\ \lbrace\ 2^e\ :\ 1\le e\le k,\ 3\mid n_{\text{odd}}\ \rbrace.
$$

(That last set accounts for **pure powers of two**, which appear when the odd component allows $\beta=1$, i.e. the $d=3$ factor is present.)

Putting these together for all $3\le n\le N$ and summing the union yields $S(N)$.

---

## 4. Techniques used to increase algorithmic efficiency

- **Reuse across all n:** Precompute $\mathcal{O}(d)$ once for each odd $d\le N$; then assemble periods for any $n$ via set/LCM operations.
- **Exact orders via factorization:** Compute $ord(\beta)$ by reducing exponents dividing $2^{m'}-1,$ using a pre-sieved prime table to factor these integers and standard order reduction.
- **Finite fields over GF(2):** Represent $\mathbb{F}_{2^m}$ as polynomials modulo an irreducible $f(x)$ of degree $m$; multiplication and powering are done with bit-operations.
- **Cheap LCM-closure:** Maintain the growing set of LCMs; sets stay small because each $\mathcal{O}(d)$ is small and $N=100$ limits $m'$.
