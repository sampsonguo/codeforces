# Problem: https://codeforces.com/contest/2241/problem/B
#
# Solution:
# Let k be the number of digits of x. Choose y = 10^k + 1.
# Then x * y = x * 10^k + x, which is just the decimal representation
# of x written twice (e.g. 73 * 101 = 7373).
# Since x is good (at most 2 distinct digits), x * y uses the same
# digits as x, so it is also good.
# y = 100...001 has only digits 1 and 0, so y is good too.

import sys


def solve():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        x = data[i]
        k = len(x)
        y = 10**k + 1
        out.append(str(y))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
