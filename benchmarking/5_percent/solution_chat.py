import math

def P_black(R, B):
    # If R is odd, parity prevents reaching all-black
    if R % 2 == 1:
        return 0.0
    x = R // 2
    # Use: P = 1 - B(1/2, x+B)/B(1/2, x)
    # Compute via log-gamma for numerical stability:
    ln_ratio = (math.lgamma(x + B) + math.lgamma(x + 0.5)
                - math.lgamma(x + B + 0.5) - math.lgamma(x))
    return 1.0 - math.exp(ln_ratio)

ans = P_black(24690, 12345)
print(f"{ans:.10f}")
