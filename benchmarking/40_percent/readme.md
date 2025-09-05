# Overview [not yet reviewed]

**Problem link:** [Project Euler Problem 854](https://projecteuler.net/problem=854)  

---

## 1. Problem statement

For every positive integer $n$, the Fibonacci sequence modulo $n$ is periodic; the period is the **Pisano period** $\pi(n)$.
Define $M(p)$ as the largest integer $n$ such that $\pi(n) = p$ (and set $M(p)=1$ if no such $n$ exists).
Define the product
$$
P(N) = \prod_{p=1}^{N} M(p).
$$
You are given $P(10)=264$. The task is to compute
$$
P(1{,}000{,}000) \bmod 1{,}234{,}567{,}891.
$$

---

## 2. High-level solution idea

Two handy simplifications make the product easy:

1. Odd periods basically never show up. For every modulus greater than two, the period length is even. So for any odd period other than three, there’s no modulus that has that period, which means the “maximizer” is just one. The only odd period that actually occurs is three (coming from modulus two), and its maximizer is two.

2. Exact rule for even periods. When the period is twice some index t, the largest modulus with exactly that period is:

   - the Lucas number at index t when t is odd, and

   - the Fibonacci number at index t when t is even.

Putting it together: To compute the desired product for a given N, work modulo 1,234,567,891. If N is at least three, start your running product at two; otherwise start at one. Then, for each t from one up to the whole-number part of N divided by two, multiply by the Lucas number at t when t is odd, and by the Fibonacci number at t when t is even, reducing modulo the target after each multiplication.

Implementation note: Iterate through t = 1, 2, … up to the limit, update the Fibonacci and Lucas sequences using their standard two-term recurrences under the modulus, and at each step multiply the appropriate term into the running product.

---

## 3. The math behind the solution

Let
$$
A=\begin{pmatrix}1&1\\[2pt]1&0\end{pmatrix},
\qquad
A^k=\begin{pmatrix}F_{k+1}&F_k\\[2pt]F_k&F_{k-1}\end{pmatrix}.
$$
Modulo $n$, the Fibonacci sequence has period dividing $p$ exactly when $A^p\equiv I\pmod n$.
Analysis of this matrix congruence yields three facts we use:

**Evenness of periods:** 

For $n>2$, $\pi(n)$ is even, so no odd $p$ occur except $p=3$ (realized by $n=2$).

**Maximal modulus at $p=2t$:**

One can show that the largest $n$ with $A^{2t}\equiv I\pmod n$ equals
$$
\gcd\big(F_{2t},\ F_{2t-1}-1,\ F_{2t+1}-1\big).
$$
Using identities $F_{2t}=F_tL_t$ and
$F_{2t\pm1}=F_{t\pm1}^2+F_t^2,$
together with standard $\gcd$ properties of Fibonacci/Lucas numbers, this gcd simplifies to
$$
\begin{cases}
F_t, & t\ \text{even},\\[2pt]
L_t, & t\ \text{odd},
\end{cases}
$$
and moreover the resulting modulus indeed has **exact** period $2t$.

**Odd-period exception:** 

$\pi(2)=3$ gives $M(3)=2$; for all other odd $p$ we have $M(p)=1$.

Therefore, $$ P(N)\equiv \big(\mathbf{1}_{N\ge 3}\cdot 2\big) \cdot \prod_{t=1}^{\lfloor N/2\rfloor} \big(\,L_t\ \text{if } t\text{ odd, else } F_t\,\big) \pmod{1{,}234{,}567{,}891}. $$

---

## 4. Techniques used to increase algorithmic efficiency

- **No brute force on periods:** We never compute $\pi(n)$ for any $n$.
  Instead, we use the closed forms for $M(p)$ and multiply them directly.
- **Streaming recurrences:** Update $F_t$ and $L_t$ via
  $F_{t+1}=F_t+F_{t-1} \ (\bmod m),\quad L_{t+1}=L_t+L_{t-1} \ (\bmod m),$
  which is $O(1)$ per step with constant memory.
- **Single pass:** A single linear pass over $t\le \lfloor N/2\rfloor$ suffices; total time is
  $O(N)$ and space is $O(1)$.
- **Early constants:** The only odd-period factor is a one-time factor 2 when $N\ge 3$, matching the given check $P(10)=264$.

---
