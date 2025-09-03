# Beautiful Graphs — Solution Overview

---

## 1. Problem statement

We are given labeled vertices \(1,2,\ldots,n\). Between each unordered pair there is exactly one of:
- a **red** directed edge one way and a **blue** directed edge the other way;
- a **green** undirected edge;
- a **brown** undirected edge.

A graph is **beautiful** iff
- a cycle has a red edge **iff** it also has a blue edge;
- there is **no** triangle that is all green or all brown.

Let \(G(n)\) be the number of beautiful graphs on \(n\) labeled vertices. Compute \(G(10^7)\) modulo \(10^9+7\).

---

## 2. High‑level solution idea

Partition the vertices into **ordered blocks** (clusters) so that:
- **Within a block:** all edges are green/brown only (no red/blue inside the block).
- **Between two distinct blocks:** all edges are red/blue with a **consistent direction** from the earlier block to the later block.

The red/blue consistency across blocks forces the block‑level orientation to be **acyclic**, thus equivalent to a **total order** on blocks (red forward, blue backward). Inside each block we must color the complete graph with green/brown **without any monochromatic triangle**.

By Ramsey’s theorem \(R(3,3)=6\), any green/brown coloring of \(K_s\) with \(s\ge 6\) contains a monochromatic triangle, so valid block sizes are at most 5.

Let \(H(s)\) be the number of green/brown colorings of \(K_s\) with **no monochromatic triangle**; then
$$H(1)=1,\quad H(2)=2,\quad H(3)=6,\quad H(4)=18,\quad H(5)=12,\quad H(s)=0\ (s\ge 6).$$

Counting beautiful graphs reduces to counting **ordered set partitions** with block weights \(H(s)\).

---

## 3. The math behind the solution

If the block sizes are \(s_1,\dots,s_k\) with \(\sum s_i=n\), then:
- choose the ordered blocks and assign labels: \(\dfrac{n!}{\prod_i s_i!}\);
- multiply the within‑block choices: \(\prod_i H(s_i)\).

Hence
$$
G(n)=\sum_{s_1+\cdots+s_k=n}\frac{n!}{\prod_i s_i!}\prod_i H(s_i).
$$

Using exponential generating functions, let
$$
B(x)=\sum_{s=1}^{5} H(s)\,\frac{x^s}{s!},\qquad
F(x)=\sum_{n\ge 0}\frac{G(n)}{n!}x^n.
$$
The “ordered sequence of blocks” construction gives
$$
F(x)=\frac{1}{1-B(x)}.
$$

Writing \(F(n)=G(n)/n!\) with \(F(0)=1\), we obtain the constant‑coefficient recurrence
$$
F(n)=\sum_{s=1}^{\min(5,n)} \frac{H(s)}{s!}\,F(n-s).
$$
Substituting the \(H(s)\) values yields
$$
F(n)=F(n-1)+F(n-2)+F(n-3)+\tfrac{3}{4}F(n-4)+\tfrac{1}{10}F(n-5).
$$
Finally,
$$
G(n)=n!\,F(n).
$$
For computations modulo a prime \(p=10^9+7\), the rational coefficients are interpreted via modular inverses: \(\tfrac{3}{4}\equiv 3\cdot 4^{-1}\pmod p\) and \(\tfrac{1}{10}\equiv 10^{-1}\pmod p\).

---

## 4. Techniques used to increase algorithmic efficiency

- **Linear recurrence with constant width:** compute \(F(n)\) in a single pass using only the last 5 values (\(\mathcal{O}(n)\) time, \(\mathcal{O}(1)\) space).
- **Streaming factorial:** update \(n!\) alongside \(F(n)\) to obtain \(G(n)=n!F(n)\) modulo \(10^9+7\).
- **No brute force over graphs:** the block decomposition plus Ramsey bound \(R(3,3)=6\) eliminates any need to enumerate edges or graphs.
- **Constant number of modular multiplies/adds per step:** only two modular inverses are needed (for \(4\) and \(10\)), computed once via Fermat’s little theorem.
