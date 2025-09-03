def solve():
    N = 10 ** 7

    # Generate sequence S_n = S_{n-1}^2 mod 50515093
    S = [0] * N
    S[0] = 290797
    for i in range(1, N):
        S[i] = (S[i - 1] * S[i - 1]) % 50515093

    # Get the sorted configuration
    sorted_S = sorted(S)

    # Calculate total steps using flow method
    total_steps = 0
    cumulative_flow = 0

    for i in range(N - 1):
        # Cumulative difference at position i
        cumulative_flow += S[i] - sorted_S[i]
        # Add positive flow to total
        if cumulative_flow > 0:
            total_steps += cumulative_flow

    return total_steps


print(solve())