# Computes X(10^18) for Project Euler "XOR-product" problem.

def X_of_N(N: int) -> int:
    # Polynomials over GF(2) are bitmasks: bit i is coeff of x^i.
    # Recurrence for t^n = A_n + t*B_n in GF(2)[t, t^{-1}]:
    # A_{n+1} = B_n
    # B_{n+1} = A_n + x*B_n   (=> XOR with left shift by 1)
    A, B = 1, 0   # A_0 = 1, B_0 = 0  (i.e., t^0 = 1)
    ans = 0

    while True:
        # advance n -> n+1
        A, B = B, A ^ (B << 1)

        # b_k = (1+x)·B_k  =>  B_k ^ (B_k << 1)
        b = B ^ (B << 1)
        if b > N:
            break
        ans ^= b

    return ans


def main():
    # Optional sanity check from the statement:
    assert X_of_N(10) == 5
    # The requested value:
    print(X_of_N(10**18))


if __name__ == "__main__":
    main()
