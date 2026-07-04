# Problem: https://codeforces.com/contest/2241/problem/G
#
# Solution:
# For a subarray b = [b_1, ..., b_m], let g_i = gcd(b_1,...,b_i).
# The minimum possible range f(b) equals d_k, where k is the first index
# with g_k < g_{k-1} (the first place the prefix gcd drops).
#
# Proof sketch:
# - Element b_i can be changed by any integer multiple of g_{i-1}, so the
#   closest value to b_1 reachable for b_i is at distance
#       d_i = min(b_i mod g_{i-1}, g_{i-1} - b_i mod g_{i-1}).
# - At the first drop, g_k = gcd(g_{k-1}, b_k) divides d_k, so d_k >= g_k.
# - After the drop, all later d_i are < g_k / 2 <= d_k.
# - Therefore f(b) = d_k.
#
# Since g_{k-1} = b_1 before the first drop, k is simply the first index
# after l with a_l not dividing a_k, and
#       f = min(a_k mod a_l, a_l - a_k mod a_l).
#
# For fixed left endpoint l, every subarray [l, r] with r >= k has the same
# contribution f. Hence l contributes (n - k + 1) * f to the answer.
#
# We find k for each l by binary searching the first position where the
# range gcd drops below a_l, using a sparse table for O(1) range gcd.

import math
import sys


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

        # Sparse table for range gcd
        LOG = n.bit_length()
        st = [[0] * (n + 2) for _ in range(LOG)]
        for i in range(1, n + 1):
            st[0][i] = a[i]
        for k in range(1, LOG):
            step = 1 << (k - 1)
            length = 1 << k
            for i in range(1, n - length + 2):
                st[k][i] = math.gcd(st[k - 1][i], st[k - 1][i + step])

        # log2 table for range queries
        lg = [0] * (n + 2)
        for i in range(2, n + 2):
            lg[i] = lg[i // 2] + 1

        def range_gcd(l, r):
            k = lg[r - l + 1]
            return math.gcd(st[k][l], st[k][r - (1 << k) + 1])

        ans = 0
        for l in range(1, n + 1):
            if a[l] == 1:
                continue
            if range_gcd(l, n) == a[l]:
                continue
            lo, hi = l + 1, n
            while lo < hi:
                mid = (lo + hi) // 2
                if range_gcd(l, mid) < a[l]:
                    hi = mid
                else:
                    lo = mid + 1
            r = lo
            rem = a[r] % a[l]
            d = min(rem, a[l] - rem)
            ans += (n - r + 1) * d

        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
