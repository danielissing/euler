import sys


def solve():
    """
    This function solves Project Euler Problem 343 by generating solutions
    from a linear recurrence relation and calculating their XOR sum.

    The problem's equation, when interpreted using polynomials over GF(2), simplifies
    and reveals that all solutions can be generated from a base case.
    This leads to an integer recurrence:
    v_0 = 0
    v_1 = 3
    v_{k+1} = (v_k << 1) ^ v_{k-1}  (for k >= 1)

    The pairs (a, b) satisfying 0 <= a <= b <= N are given by (v_n, v_{n+1})
    for n >= 0, as long as v_{n+1} <= N. We need to find the XOR sum of the
    'b' values, which are the terms v_1, v_2, v_3, ... up to N.
    """
    N = 10 ** 18

    # Initialize the first two terms of the sequence
    v_prev = 0  # This represents v_0
    v_curr = 3  # This represents v_1

    # The 'b' values in the solutions (a,b) are v_1, v_2, v_3, ...
    # We compute the XOR sum of these values up to the limit N.
    xor_sum_of_b = 0

    # The first 'b' value is v_1
    if v_curr <= N:
        xor_sum_of_b ^= v_curr

    # Generate subsequent terms and update the XOR sum
    while True:
        # Calculate the next term in the sequence
        v_next = (v_curr << 1) ^ v_prev

        # Stop if the term exceeds the limit N
        if v_next > N:
            break

        # Include the new term in the XOR sum
        xor_sum_of_b ^= v_next

        # Update the terms for the next iteration
        v_prev = v_curr
        v_curr = v_next

    print(xor_sum_of_b)


if __name__ == "__main__":
    solve()
