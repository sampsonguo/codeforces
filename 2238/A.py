# Problem: https://codeforces.com/contest/2238/problem/A
#
# Solution:
# We can only decrease elements of a, and we may pay c to reorder a once.
# The optimal strategy is one of:
#   1. Do not reorder: feasible iff a[i] >= b[i] for all i.
#      Cost = sum(a[i] - b[i]).
#   2. Reorder a (and conceptually sort b) so that the i-th smallest a
#      matches the i-th smallest b.  Feasible iff a_sorted[i] >= b_sorted[i]
#      for all i.  Cost = c + sum(a_sorted[i] - b_sorted[i]).
# Reordering more than once never helps, and subtracting before reordering
# can only make matching harder, so these two pure strategies are enough.
# Answer the smaller feasible cost, or -1 if neither works.

import sys


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        c = int(next(it))
        a = [int(next(it)) for _ in range(n)]
        b = [int(next(it)) for _ in range(n)]

        best = None

        # Option 1: subtract in place.
        if all(x >= y for x, y in zip(a, b)):
            best = sum(x - y for x, y in zip(a, b))

        # Option 2: pay c to reorder, then subtract.
        a_sorted = sorted(a)
        b_sorted = sorted(b)
        if all(x >= y for x, y in zip(a_sorted, b_sorted)):
            cost2 = c + sum(x - y for x, y in zip(a_sorted, b_sorted))
            if best is None or cost2 < best:
                best = cost2

        out.append(str(best if best is not None else -1))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
