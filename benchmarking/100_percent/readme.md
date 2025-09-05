# Overview [not yet reviewed]

**Problem link:** [Project Euler Problem 812](https://projecteuler.net/problem=812)  

## 1. **Problem statement**  
Given a monic integer polynomial $f(x)$, call it *dynamical* if $f(x)$ divides $f(x^2-2)$. Let $S(n)$ be the number of degree- $n$ dynamical polynomials. Examples: $S(2)=6$, $S(5)=58$, $S(20)=122087$. 

**Task:** Compute $S(10{,}000)$ modulo $998244353$.

## 2. **High-level solution idea**  
Use the conjugacy $x=t+t^{-1}$, under which the map $x\mapsto x^2-2$ becomes $t\mapsto t^2$. With

$$
F(t)=t^n\,f(t+t^{-1}),
$$

the divisibility $f(x)\mid f(x^2-2)$ is equivalent to

$$
F(t)\ \mid\ F(t^2).
$$

This forces $F$ to be a product of cyclotomic polynomials with multiplicities constrained along dyadic chains. Counting such factorizations reduces to extracting a coefficient of an Euler product (a generating function), with a small parity correction for the chain rooted at $1$.

## 3. **The math behind the solution**  

**Cyclotomic structure** 

Write

$$
F(t)=\prod_{d\ge1}\Phi_d(t)^{e_d},\qquad \deg F=\sum_d e_d\,\varphi(d)=2n.
$$

From $F(t)\mid F(t^2)$ one obtains the *chain constraints*

$$
e_{2k}\le e_k\quad(\forall\,k\ge1),
$$

and reciprocity forces $e_1$ to be even.

**Dyadic chains** 

Group indices by odd roots $m$: $d_s=2^s m$ with weights $w_s=\varphi(d_s)$. The partial sums along a chain are

$$
W_t=\sum_{j=0}^{t}w_j=\varphi(m)\cdot 2^t.
$$

Nonincreasing exponents along a chain yield the chain generating function

$$
\prod_{t\ge0}\frac{1}{1-q^{W_t}}.
$$

**Parity factor for $m=1$**

The constraint “ $e_1$ even ” projects the chain onto even multiplicity:

$$
\frac{1}{2}\left(\prod_{t\ge0}\frac{1}{1-q^{2^t}}+\prod_{t\ge0}\frac{1}{1+q^{2^t}}\right).
$$

**Euler product over odd $m\ge3$** 

Collapsing all chains with odd $m\ge3$ gives

$$
\prod_{\substack{m\ge3\\ m\ \text{odd}}}\ \prod_{t\ge0}\frac{1}{1-q^{\varphi(m)\,2^t}}
\ =\ \prod_{k\ge1}(1-q^k)^{-A_k},
$$

where

$$
A_k=\sum_{s=0}^{v_2(k)} b\!\left(\frac{k}{2^s}\right),\qquad
b(t)=num\lbrace\{\text{odd }m\ge1:\ \varphi(m)=t\}\rbrace.
$$

(We effectively exclude $m=1$ by omitting the contribution at $t=1$.)

**Putting it together** 

Denote by $G_{\mathrm{odd}}(q)$ the Euler product $\prod_k(1-q^k)^{-A_k}$ and by $P(q)$ the parity factor above. Then

$$
S(n)=\big[q^{\,2n}\big]\ \Big( G_{\mathrm{odd}}(q)\cdot P(q)\Big).
$$

## 4. **Techniques used to increase algorithmic efficiency**  
- **Counting $\varphi$-preimages without scanning $m$.** Exploit multiplicativity $\varphi(p^a)=(p-1)p^{a-1}$ for odd primes to enumerate products of $(p-1)p^{a-1}$ by DFS, obtaining $b(t)=num\lbrace\{\text{odd }m:\varphi(m)=t\}\rbrace$ for all $t\le 2n$, instead of iterating $m$.  
- **Building the exponents $A_k$ correctly.** For each $k\le 2n$, repeatedly halve $k$ while even and accumulate $b(\cdot)$; never floor-divide by $2$ unless $k$ is divisible by $2$. This enforces the dyadic-chain constraint precisely.  
- **Euler transform via series $\log$ and $\exp$.** Using $\log\Big(\prod_{k\ge1}(1-q^k)^{-A_k}\Big)\ =\ \sum_{m\ge1}\frac{1}{m}\!\sum_{d\mid m} dA_d\ q^m$, compute the logarithm coefficients $C[m]=\tfrac{1}{m}\sum_{d\mid m}dA_d$ and recover $G_{\mathrm{odd}}(q)=\exp\!\big(\sum_{m\ge1}C[m]q^m\big)$.
- **Fast power-series arithmetic.** Use NTT-based convolution modulo $998244353$ to support quasi-linear polynomial multiplication, plus Newton-style routines for series inverse/log/exp.  
- **Efficient parity factor.** Compute $\prod(1\mp q^{2^t})^{-1}$ up to degree $2n$ by residue-class DP: prefix sums for $1/(1-q^w)$ and alternating prefix sums for $1/(1+q^w)$.  
- **Small-case checks.** Verify $S(2)=6$, $S(5)=58$, $S(20)=122087$ before evaluating $S(10000)$.
