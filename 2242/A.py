# Problem: https://codeforces.com/contest/2242/problem/A
#
# Solution:
# We can construct a valid string iff one of the following holds:
# 1. Some letter appears at least 3 times -> put three of them together
#    (e.g. "aaa"), creating at least two equal "aa" bigrams.
# 2. At least two different letters appear at least twice -> arrange them
#    as "abab...", creating at least two equal "ab" bigrams.
# Otherwise every letter appears at most twice and at most one letter
# appears twice, so no two equal bigrams are possible.

import sys


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        k = int(data[idx])
        idx += 1
        c = list(map(int, data[idx : idx + k]))
        idx += k
        max_cnt = max(c)
        pairs = sum(1 for x in c if x >= 2)
        if max_cnt >= 3 or pairs >= 2:
            out.append("YES")
        else:
            out.append("NO")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
