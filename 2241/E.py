# Problem: https://codeforces.com/contest/2241/problem/E
#
# Solution:
# For any three vertices in a tree, either:
# 1. They are collinear (one lies on the path between the other two):
#    then p(u,v)*p(v,w)*p(w,u) is always a perfect square.
# 2. They branch at a median vertex m (m is not one of the three):
#    then the product equals (product of the three branches)^2 * a_m^3,
#    so it is a perfect square iff a_m itself is a perfect square.
#
# Therefore:
# answer = C(n,3) - sum over vertices m with a_m NOT square of branch(m)
# where branch(m) is the number of triplets whose median is m,
# i.e. the number of ways to pick one vertex from three different
# components of the tree after removing m.

import math
import sys


def is_square(x):
    if x < 0:
        return False
    r = math.isqrt(x)
    return r * r == x


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        a = [0] + list(map(int, data[idx : idx + n]))
        idx += n
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u = int(data[idx])
            v = int(data[idx + 1])
            idx += 2
            adj[u].append(v)
            adj[v].append(u)

        # Iterative DFS to get parent and processing order
        parent = [0] * (n + 1)
        order = []
        stack = [1]
        parent[1] = -1
        while stack:
            u = stack.pop()
            order.append(u)
            for v in adj[u]:
                if v != parent[u]:
                    parent[v] = u
                    stack.append(v)

        subtree = [1] * (n + 1)
        for u in reversed(order):
            for v in adj[u]:
                if v != parent[u]:
                    subtree[u] += subtree[v]

        total = n * (n - 1) * (n - 2) // 6
        ans = total
        for m in range(1, n + 1):
            if is_square(a[m]):
                continue
            sizes = []
            for v in adj[m]:
                if v == parent[m]:
                    sizes.append(n - subtree[m])
                else:
                    sizes.append(subtree[v])
            k = len(sizes)
            if k < 3:
                continue
            S = sum(sizes)
            S2 = sum(x * x for x in sizes)
            S3 = sum(x * x * x for x in sizes)
            branch = (S * S * S - 3 * S * S2 + 2 * S3) // 6
            ans -= branch

        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
