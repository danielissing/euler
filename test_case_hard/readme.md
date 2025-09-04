# Overview

**Problem link:** [Project Euler Problem 791](https://projecteuler.net/problem=791).

This file describes `solution_chat.py`. Neither Gemini nor Claude were able to solve this problem.

---

## 1. Problem statement

For integers $1 \le a \le b \le c \le d \le n$, set
$$
\bar{x} = \frac{a+b+c+d}{4}
$$
and let the variance be
$$
\frac{1}{4}\sum_{x\in\{a,b,c,d\}}(x-\bar{x})^2
$$
Define $S(n)$ as the **sum of all quadruples** $(a,b,c,d)$ satisfying “average = twice the variance”, i.e.
$$
\bar{x} = 2\,\mathrm{Var}
$$
Example values: $S(5)=48$ and $S(10^3)=37048340$.  
Task: compute $S(10^8) \bmod 433494437$.

---

## 2. High‑level solution idea

- Replace the variance using the pairwise‑differences identity so the condition becomes one quadratic in the entries.
- Parameterize the quadruple by nonnegative gaps $u=b-a$, $v=c-b$, $w=d-c$, then switch to symmetric variables
  $$
  A=\frac{u+w}{2}, \qquad G=\frac{u-w}{2}, \qquad t=v+A
  $$
  which encode the “outer symmetry” and the central gap.
- For each $(A,t)$, the valid $G$ form a contiguous integer interval cut out by a quadratic inequality and $|G|\le A$.
- The sum contributed by all $(A,G,t)$ at fixed $(A,t)$ reduces to
  $$
  \text{contribution}(A,t) \;=\; 2\big(A^2+t^2\big)\,N \;+\; 2\sum_{G} G^2
  $$
  where $N$ is the count of admissible $G$ and $\sum_{G}G^2$ is available in closed form.
- Accumulate these contributions over the feasible $(A,t)$ domain using only integer arithmetic with modular reduction.

---

## 3. The math behind the solution

### Variance condition $\Longleftrightarrow$ pairwise squares
Let $x_1,x_2,x_3,x_4\in\{a,b,c,d\}$ with mean $\mu$. Using
$$
\sum_{i<j}(x_i-x_j)^2 \;=\; 4\sum_{i=1}^4 (x_i-\mu)^2
$$
the condition $\mu = 2\cdot \mathrm{Var}$ becomes
$$
\sum_{i<j}(x_i-x_j)^2 \;=\; 2(a+b+c+d)
$$

### Gap parameterization
Set $u=b-a$, $v=c-b$, $w=d-c$ (all $\ge 0$). A direct expansion yields
$$
\sum_{i<j}(x_i-x_j)^2
= 3u^2 + 4v^2 + 3w^2 + 4uv + 2uw + 4vw
$$
Also $s:=a+b+c+d = 4a+3u+2v+w$. Plugging in gives a linear equation for $a$:
$$
8a \;=\; 3u^2+4v^2+3w^2+4uv+2uw+4vw \;-\; (6u+4v+2w)
$$
Therefore $a$ is uniquely determined by $(u,v,w)$, and integrality forces
$$
u \equiv w \pmod{2}
$$

### Symmetric variables
Define
$$
A=\frac{u+w}{2}\ (\ge 0),\qquad G=\frac{u-w}{2}\ (\in\mathbb{Z}),\qquad t=v+A\ (\ge A)
$$
Condition above guarantees $A,G\in\mathbb{Z}$ with $|G|\le A$. Two key simplifications follow:

1. The sum of the quadruple becomes
   $$
   s \;=\; a+b+c+d \;=\; 2\big(A^2 + t^2 + G^2\big)
   $$

2. The bound $d\le n$ is equivalent to a quadratic window for $G$:
   $$
   G(G-1) \;\le\; T(A,t), \qquad T(A,t) := 2n - \big(A^2 + t^2 + A + t\big)
   $$

Thus, for fixed $(A,t)$, admissible $G$ are the integers with
$$
|G|\le A \quad\text{and}\quad G(G-1)\le T(A,t)
$$

### Closed forms per $(A,t)$
Let
$$
U=\left\lfloor\frac{1+\sqrt{1+4T}}{2}\right\rfloor,\qquad
R=\left\lfloor\frac{\sqrt{1+4T}-1}{2}\right\rfloor \quad(\text{so } U=R+1)
$$
Then
$$
L_{\text{pos}}=\min(A,U),\qquad L_{\text{neg}}=\min(A,R)
$$
and therefore
$$
N \;=\; 1 + L_{\text{pos}} + L_{\text{neg}}, \qquad
\sum_{G} G^2 \;=\; \frac{L_{\text{pos}}(L_{\text{pos}}+1)(2L_{\text{pos}}+1)}{6}
\;+\; \frac{L_{\text{neg}}(L_{\text{neg}}+1)(2L_{\text{neg}}+1)}{6}
$$
By the expression for $s$ above, the total contribution from this $(A,t)$ is
$$
\text{contribution}(A,t)=2\big(A^2+t^2\big)\,N \;+\; 2\sum_{G} G^2
$$

### Domain of $(A,t)$ and edge corrections
From $T(A,t)\ge 0$ we get
$$
A\ge 0,\qquad t\ge A,\qquad t^2+t \le 2n - (A^2 + A)
$$
Finally, enforcing $a\ge 1$ eliminates exactly the $a=0$ cases, which occur at
$$
(A,t,G)\in \{(0,1,0),\ (1,1,0),\ (1,1,1)\}
$$
(When present, subtract their contributions $2\big(A^2+t^2+G^2\big)$ once.)

---

## 4. Techniques used to increase algorithmic efficiency

- **Integer‑only arithmetic:** All formulas use exact integers with $\mathrm{isqrt}$; no floating point is needed.
- **Range splitting for $t$:** For each $A$, the thresholds where $U$ or $R$ reaches $A$ create three regimes:
  1. **Both sides saturated:** $L_{\text{pos}}=L_{\text{neg}}=A$.
  2. **Positive side saturated only:** $L_{\text{pos}}=A$, $L_{\text{neg}}=A-1$.
  3. **Unsaturated tail:** $L_{\text{pos}}=U$, $L_{\text{neg}}=U-1$ with $U$ decreasing stepwise.
  The first two admit block sums via $\sum t^2$; the last uses block stepping until $U$ drops, yielding $O(1)$ amortized per block.
- **Closed‑form inner sums:** Use $\sum_{g=1}^{m} g^2 = \dfrac{m(m+1)(2m+1)}{6}$ and $\sum_{i=0}^{s-1}(t_0+i)^2$ to aggregate many $t$ at once.
- **Tight search space:** From the domain constraints, $A$ and $t$ are $O(\sqrt{n})$; with splitting and blocks, the total work is $\tilde{O}(\sqrt{n})$.
- **Modular accumulation:** All contributions are reduced modulo $433494437$ on the fly.
