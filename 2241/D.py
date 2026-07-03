# Problem: https://codeforces.com/contest/2241/problem/D
#
# Solution (greedy from right to left):
# Let d[i] = a[i] - b[i].
# - If d[i] < 0 we can fix position i locally with [i, i] operations,
#   which only increase a[i].
# - If d[i] > 0 we must decrease a[i]. The only way is to include i as
#   an odd offset in some operation, e.g. [i-1, i]. That decreases a[i]
#   by 1 and increases a[i-1] by 1, so the excess is pushed leftwards.
# Process from right to left, pushing positive excess to the left.
# At the end, position 0 can only be increased, so we need d[0] <= 0.

import sys


def solve():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = list(map(int, data[idx : idx + n]))
        idx += n
        b = list(map(int, data[idx : idx + n]))
        idx += n
        d = [a[i] - b[i] for i in range(n)]
        for i in range(n - 1, 0, -1):
            if d[i] > 0:
                d[i - 1] += d[i]
        out.append("YES" if d[0] <= 0 else "NO")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
