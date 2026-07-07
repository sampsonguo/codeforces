# Problem: https://codeforces.com/contest/2242/problem/B
#
# Solution:
# The array only contains 1, 2, 3.
# Split into three contiguous non-empty parts [1..i], [i+1..j], [j+1..n].
#
# Condition for part i (1-indexed part number):
#   number of elements greater than i  <=  half of the part length.
# So:
#   part 1: count(2)+count(3) <= count(1)      (1's are at least half)
#   part 2: count(3) <= count(1)+count(2)      (3's are at most half)
#   part 3: always OK.
#
# Define prefix balances:
#   F[k] = (#1 up to k) - (#2 + #3 up to k)
#   D[k] = (#3 up to k) - (#1 + #2 up to k)
#
# A first cut at i is valid iff F[i] >= 0.
# For such i, the middle part [i+1..j] is valid iff
#   (#3 in [i+1..j]) <= (#1+#2 in [i+1..j])
# which simplifies to D[j] <= D[i].
#
# Precompute suffix minima of D. Then for every possible first cut i,
# check whether there exists j in [i+1, n-1] with D[j] <= D[i].
# If yes for any i, answer YES, otherwise NO.

import sys


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = list(map(int, data[idx : idx + n]))
        idx += n

        F = [0] * (n + 1)
        D = [0] * (n + 1)
        c1 = c2 = c3 = 0
        for i, v in enumerate(a, start=1):
            if v == 1:
                c1 += 1
            elif v == 2:
                c2 += 1
            else:
                c3 += 1
            F[i] = c1 - c2 - c3
            D[i] = c3 - c1 - c2

        # suffix_min[k] = min(D[k..n-1])
        INF = 10**9
        suffix_min = [INF] * (n + 2)
        for k in range(n - 1, 0, -1):
            suffix_min[k] = min(D[k], suffix_min[k + 1])

        ok = False
        # first part ends at i, middle must have at least one element,
        # right part must have at least one element.
        for i in range(1, n - 1):
            if F[i] >= 0 and suffix_min[i + 1] <= D[i]:
                ok = True
                break

        out.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
