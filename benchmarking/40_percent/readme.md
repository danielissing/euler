# Overview

**Context:** This note explains the reasoning behind the Python script that computes
$$P(1{,}000{,}000) \bmod 1{,}234{,}567{,}891$$ for the Pisano-period product function.

---

## 1. Problem statement

For every positive integer $$n$$, the Fibonacci sequence modulo $$n$$ is periodic; the period is the **Pisano period** $$\pi(n)$$.
Define $$M(p)$$ as the largest integer $$n$$ such that $$\pi(n) = p$$ (and set $$M(p)=1$$ if no such $$n$$ exists).
Define the product
$$
P(N) = \prod_{p=1}^{N} M(p).
$$
You are given $$P(10)=264$$. The task is to compute
$$
P(1{,}000{,}000) \bmod 1{,}234{,}567{,}891.
$$

---

## 2. High-level solution idea

Two key simplifications collapse the product:

1) **Odd periods almost never occur.** It is known that $$\pi(n)$$ is even for all $$n>2$$.
   Hence, for odd $$p\neq 3$$ there is no $$n$$ with $$\pi(n)=p$$ and thus $$M(p)=1$$.
   The only odd period that occurs is $$\pi(2)=3$$, giving $$M(3)=2$$.

2) **Closed form for maximizers at even periods.** Writing $$p=2t$$,
   the maximal modulus with period exactly $$2t$$ is
   $$
   M(2t)=\begin{cases}
     L_t, & t\ \text{odd},\\[2pt]
     F_t, & t\ \text{even},
   \end{cases}
   $$
   where $$F_t$$ and $$L_t$$ are the Fibonacci and Lucas numbers respectively.

Therefore,
$$
P(N)\equiv \big(\mathbf{1}_{N\ge 3}\cdot 2\big)
\cdot \prod_{t=1}^{\lfloor N/2\rfloor} \big(\,L_t\ \text{if } t\text{ odd, else } F_t\,\big) \pmod{1{,}234{,}567{,}891}.
$$

The implementation simply streams through $$t=1,2,\ldots,\lfloor N/2\rfloor$$,
updates $$F_t$$ and $$L_t$$ via their linear recurrences modulo the target,
and multiplies the appropriate term into the running product.

---

## 3. The math behind the solution

Let
$$
A=\begin{pmatrix}1&1\\[2pt]1&0\end{pmatrix},
\qquad
A^k=\begin{pmatrix}F_{k+1}&F_k\\[2pt]F_k&F_{k-1}\end{pmatrix}.
$$
Modulo $$n$$, the Fibonacci sequence has period dividing $$p$$ exactly when $$A^p\equiv I\pmod n$$.
Analysis of this matrix congruence yields three facts we use:

- **Evenness of periods:** For $$n>2$$, $$\pi(n)$$ is even, so no odd $$p$$ occur except $$p=3$$ (realized by $$n=2$$).
- **Maximal modulus at $$p=2t$$:** One can show that the largest $$n$$ with $$A^{2t}\equiv I\pmod n$$ equals
  $$
  \gcd\big(F_{2t},\ F_{2t-1}-1,\ F_{2t+1}-1\big).
  $$
  Using identities $$F_{2t}=F_tL_t$$ and
  $$F_{2t\pm1}=F_{t\pm1}^2+F_t^2,$$
  together with standard $$\gcd$$ properties of Fibonacci/Lucas numbers, this gcd simplifies to
  $$
  \begin{cases}
    F_t, & t\ \text{even},\\[2pt]
    L_t, & t\ \text{odd},
  \end{cases}
  $$
  and moreover the resulting modulus indeed has **exact** period $$2t$$.
- **Odd-period exception:** $$\pi(2)=3$$ gives $$M(3)=2$$; for all other odd $$p$$ we have $$M(p)=1$$.

Putting these together gives the closed product for $$P(N)$$ above.

---

## 4. Techniques used to increase algorithmic efficiency

- **No brute force on periods:** We never compute $$\pi(n)$$ for any $$n$$.
  Instead, we use the closed forms for $$M(p)$$ and multiply them directly.
- **Streaming recurrences:** Update $$F_t$$ and $$L_t$$ via
  $$F_{t+1}=F_t+F_{t-1} \ (\bmod m),\quad L_{t+1}=L_t+L_{t-1} \ (\bmod m),$$
  which is $$O(1)$$ per step with constant memory.
- **Single pass:** A single linear pass over $$t\le \lfloor N/2\rfloor$$ suffices; total time is
  $$O(N)$$ and space is $$O(1)$$.
- **Early constants:** The only odd-period factor is a one-time factor 2 when $$N\ge 3$$, matching the given check $$P(10)=264$$.

---
