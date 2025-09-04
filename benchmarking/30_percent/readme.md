# Overview [**not** yet reviewed]

**Problem link:** [Project Euler Problem 839](https://projecteuler.net/problem=839)  

---

## 1. Problem statement

We define a sequence by
$$S_0 = 290797, \quad S_{n} = S_{n-1}^2 \bmod 50515093\ \text{ for } n>0.$$
There are bowls indexed \(0,1,\dots,N-1\). Initially bowl \(n\) contains \(a_n = S_n\) beans.

At each step, find the smallest index \(n\) with \(a_n > a_{n+1}\) and move one bean from bowl \(n\) to bowl \(n+1\).
Let \(B(N)\) be the number of steps until the configuration becomes non‑decreasing.

Examples: \(B(5)=0\), \(B(6)=14263289\), \(B(100)=3284417556\).  
**Task:** Compute \(B(10^7)\).

---

## 2. High-level solution idea

Track the “potential”
$$P(a) \;=\; \sum_{i=0}^{N-1} i\,a_i.$$
A single move replaces \((a_i, a_{i+1})\) by \((a_i-1, a_{i+1}+1)\), so
$$\Delta P \;=\; \big(i(a_i-1) + (i+1)(a_{i+1}+1)\big) - \big(i a_i + (i+1)a_{i+1}\big) \;=\; 1.$$
Thus **each step increases \(P\) by exactly 1**, and when the array becomes non‑decreasing, no further move is possible. Therefore
$$B(N) \;=\; P(a^*) - P(a),$$
where \(a^*\) is the *closest* non‑decreasing array reachable by redistributing beans via adjacent moves.

We obtain \(a^*\) by running **isotonic regression** (Pool‑Adjacent‑Violators, PAVA) on the initial slopes \(a_i=S_i\). PAVA produces contiguous blocks whose values are all set to the block’s average. Because beans are integers and moves are discrete, we then **integerize** each block average by distributing
$$q=\left\lfloor \frac{T}{L} \right\rfloor \quad\text{and}\quad q+1$$
over the block of length \(L\) with total \(T\), assigning \(q\) to the first \(L-r\) positions and \(q+1\) to the last \(r=T\bmod L\). If this would break global monotonicity across blocks, we merge the conflicting blocks and repeat. Finally, compute \(P(a^*)\) via arithmetic sums and subtract \(P(a)\).

---

## 3. The math behind the solution

### Potential equals step count
Let \(a\) be the current array and define
$$P(a)=\sum_{i=0}^{N-1} i\,a_i.$$
Each allowed move increases \(P\) by 1 (calculation above). If \(a^*\) is the terminal non‑decreasing configuration, the total number of moves is
$$B(N)=P(a^*)-P(a).$$

### Convex viewpoint via prefix sums
Define cumulative sums \(C(k)=\sum_{i=0}^{k-1} a_i\) for \(k=0,1,\dots,N\) with \(C(0)=0\). The slopes of \(C\) are the \(a_i\). Enforcing \(a^*\) non‑decreasing is equivalent to requiring **convexity** of the cumulative curve \(C^*\). Among all convex \(C^*\) that share endpoints \(C^*(0)=C(0)=0\), \(C^*(N)=C(N)\) and lie below \(C\), the **greatest convex minorant (GCM)** maximizes \(C^*\) pointwise and yields the isotonic‑regressed slopes \(a^*\).

PAVA constructs the GCM in linear time by merging adjacent “violator” blocks. For a final block with length \(L\) and total \(T\), the real‑valued slope is the average \(T/L\).

### Integer convexification inside a block
Because beans are integers, on a block of length \(L\) and total \(T=qL+r\) (\(0\le r<L\)), the unique maximal integer convex profile under the block’s straight line assigns
$$\underbrace{q,\dots,q}_{L-r\ \text{terms}},\ \underbrace{q+1,\dots,q+1}_{r\ \text{terms}}.$$
To maintain global monotonicity, if the last slope of the left block (which is \(q+\mathbf{1}_{r>0}\)) exceeds the first slope of the right block (which is \(\lfloor T'/L' \rfloor\)), we merge the blocks and recompute \(q, r\). This produces the integer, non‑decreasing \(a^*\) consistent with adjacent moves.

### Computing \(P(a^*)\) without expanding elements
Let a finalized block start at index \(s\) with length \(L\) and totals \(T=qL+r\). Its contribution to \(P(a^*)\) is
$$q \sum_{i=s}^{s+L-1} i \;+\; \sum_{i=s+L-r}^{s+L-1} i,$$
using the closed form
$$\sum_{i=a}^{b} i \;=\; \frac{(b-a+1)(a+b)}{2}.$$
Summing over blocks gives \(P(a^*)\). The initial potential \(P(a)=\sum i\,S_i\) is accumulated on the fly while generating \(S_i\). Finally,
$$B(N)=P(a^*)-P(a).$$

---

## 4. Techniques used to increase algorithmic efficiency

- **Isotonic regression (PAVA) in one streaming pass:** Maintain a small stack of blocks \((L,T)\). Merge while averages violate non‑decreasing order using cross‑multiplication (avoid division) to compare \(T_1/L_1\) and \(T_2/L_2\).
- **Integer rounding with a tiny second pass:** Convert each block average to \(q\)/\(q{+}1\) profile and merge only if rounding would break monotonicity across blocks.
- **Closed‑form aggregation:** Compute \(P(a^*)\) by arithmetic‑series formulas per block; no expansion to element level and no simulation of moves.
- **Streaming PRNG and potential:** Generate \(S_n\) via \(x\leftarrow x^2\bmod M\) and accumulate \(P(a)=\sum i\,S_i\) in one pass; no arrays of length \(N\).
- **Time/space:** Overall \(O(N)\) time with extremely small memory (proportional to the number of blocks, orders of magnitude smaller than \(N\)); uses only integer arithmetic from the standard library.
