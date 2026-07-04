# Problem: https://codeforces.com/contest/2241/problem/E
#
# Solution:
# For any three distinct vertices in a tree, there is a unique vertex m
# that lies on all three pairwise simple paths (the "center" of the triplet).
# - If the three vertices are collinear, m is the middle vertex.
# - If they branch, m is the junction vertex (not one of the three).
#
# Let the component sizes after removing m be c_1, c_2, ..., c_k.
# Triplets whose center is m are of two types:
#   1. {m, x, y} with x, y in two different components: count = sum_{i<j} c_i c_j
#   2. {x, y, z} with x, y, z in three different components:
#      count = sum_{i<j<l} c_i c_j c_l
#
# For either type, the product p(u,v)*p(v,w)*p(w,u) equals
# (product of the relevant branch-paths)^2 divided by (or multiplied by) a_m,
# which is a perfect square iff a_m itself is a perfect square.
#
# Therefore:
# answer = sum over vertices m with a_m square of (pair_count(m) + triple_count(m))

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

        ans = 0
        for m in range(1, n + 1):
            if not is_square(a[m]):
                continue
            sizes = []
            for v in adj[m]:
                if v == parent[m]:
                    sizes.append(n - subtree[m])
                else:
                    sizes.append(subtree[v])
            k = len(sizes)
            if k < 2:
                continue
            S = sum(sizes)
            S2 = sum(x * x for x in sizes)
            pair_count = (S * S - S2) // 2
            triple_count = 0
            if k >= 3:
                S3 = sum(x * x * x for x in sizes)
                triple_count = (S * S * S - 3 * S * S2 + 2 * S3) // 6
            ans += pair_count + triple_count

        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
