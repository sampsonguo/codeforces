# Problem: https://codeforces.com/contest/2242/problem/D
#
# Solution:
# 1. The total digit sum modulo 10 is invariant under the operation.
#    If sum(a) % 10 != sum(b) % 10, the answer is -1.
# 2. Otherwise, each final string is obtained by cutting the original string
#    into contiguous blocks and replacing every block by its digit sum mod 10.
#    Two final strings are equal iff the sequences of block sums are equal.
# 3. Let A[i] = prefix sum of a[0..i-1] mod 10, B[j] similarly.
#    A block a[i..i'-1] matches b[j..j'-1] iff
#        (A[i'] - A[i]) % 10 == (B[j'] - B[j]) % 10
#    which is equivalent to A[i'] - B[j'] == A[i] - B[j] (mod 10).
# 4. All cut points must lie on D(i,j) = (A[i] - B[j]) % 10 == 0.
#    The task becomes: longest chain of D=0 points from (0,0) to (n,m)
#    with strictly increasing coordinates.  Answer = chain size - 1.
# 5. Process i = 1..n-1.  For each i, all j with B[j] == A[i] and 1<=j<=m-1
#    are candidate intermediate points.  Use a Fenwick tree over j to keep
#    the maximum dp of already processed points, supporting prefix-max query
#    and point update.

import sys


class FenwickMax:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def update(self, idx, val):
        # idx is 1-based
        n = self.n
        bit = self.bit
        while idx <= n:
            if val > bit[idx]:
                bit[idx] = val
            idx += idx & -idx

    def query(self, idx):
        # max on [1..idx], idx is 1-based
        res = 0
        bit = self.bit
        while idx > 0:
            if bit[idx] > res:
                res = bit[idx]
            idx -= idx & -idx
        return res


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    p = 1
    for _ in range(t):
        a = data[p].decode()
        p += 1
        b = data[p].decode()
        p += 1
        n = len(a)
        m = len(b)

        # prefix sums mod 10, A[0]=B[0]=0
        A = [0] * (n + 1)
        for i, ch in enumerate(a, start=1):
            A[i] = (A[i - 1] + ord(ch) - 48) % 10
        B = [0] * (m + 1)
        for j, ch in enumerate(b, start=1):
            B[j] = (B[j - 1] + ord(ch) - 48) % 10

        if A[n] != B[m]:
            out.append("-1")
            continue

        # positions in b grouped by prefix value
        posB = [[] for _ in range(10)]
        for j in range(m + 1):
            posB[B[j]].append(j)

        # Fenwick tree over j coordinates 0..m
        # we store dp value at coordinate j at tree index j+1
        bit = FenwickMax(m + 2)
        # start point (0,0) has dp = 1
        bit.update(1, 1)

        # process intermediate i = 1 .. n-1
        for i in range(1, n):
            v = A[i]
            lst = posB[v]
            # iterate from large j to small j so that updates within the same i
            # do not interfere with each other (queries only look at smaller j)
            for j in reversed(lst):
                if j == 0 or j == m:
                    continue
                # dp = 1 + max dp of a previous boundary with j' < j
                best = bit.query(j)
                dp = best + 1
                bit.update(j + 1, dp)

        # final point (n, m)
        final_dp = bit.query(m) + 1
        out.append(str(final_dp - 1))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
