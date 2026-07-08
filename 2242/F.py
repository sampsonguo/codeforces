# Problem: https://codeforces.com/contest/2242/problem/F
#
# Solution sketch:
# For a fixed sequence, define its effect on a starting balance b as F(b).
# A day with value a transforms a balance b into T_a(b) = b+a (if b<a) or
# b-a (if b>=a).  Prepending a day a to a suffix with effect F gives a new
# effect F' = F o T_a, i.e. F'(b) = F(b+a) for b<a and F'(b-a) for b>=a.
#
# Since a_i <= n, every balance stays in [0, 2n-1].  We therefore maintain the
# array [F(0), F(1), ..., F(2n-1)] for the current suffix.  Prepending a day a
# rearranges this array as:
#     new[0..a-1]     = old[a..2a-1]
#     new[a..2n-1]    = old[0..2n-a-1]
#
# We process days from right to left, updating the array with this fold, and
# read the new first element as the answer for the current suffix.  The fold
# is implemented with a persistent implicit treap so that the piece that is
# needed twice (old[a..2a-1]) can be shared.  The treap is rebuilt from time
# to time to keep memory usage under control.
#
# The treap uses size-based merging: when merging two subtrees of sizes sz_l
# and sz_r, the left root becomes the new root with probability sz_l/(sz_l+sz_r).

import random
import sys


def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    MX = 2 * n

    # Persistent implicit treap, stored in parallel arrays.
    # Node 0 is the null node.
    val = [0]
    left = [0]
    right = [0]
    size = [0]

    def new_node(v):
        val.append(v)
        left.append(0)
        right.append(0)
        size.append(1)
        return len(val) - 1

    def copy_node(i):
        val.append(val[i])
        left.append(left[i])
        right.append(right[i])
        size.append(size[i])
        return len(val) - 1

    def upd(i):
        size[i] = 1 + size[left[i]] + size[right[i]]

    def merge(a_, b_):
        if a_ == 0:
            return b_
        if b_ == 0:
            return a_
        sz_a = size[a_]
        sz_b = size[b_]
        if random.random() * (sz_a + sz_b) < sz_a:
            a_ = copy_node(a_)
            right[a_] = merge(right[a_], b_)
            upd(a_)
            return a_
        else:
            b_ = copy_node(b_)
            left[b_] = merge(a_, left[b_])
            upd(b_)
            return b_

    def split(root, k):
        if root == 0:
            return (0, 0)
        root = copy_node(root)
        ls = size[left[root]]
        if k <= ls:
            l, r = split(left[root], k)
            left[root] = r
            upd(root)
            return (l, root)
        else:
            l, r = split(right[root], k - ls - 1)
            right[root] = l
            upd(root)
            return (root, r)

    def build(values, l, r):
        if l >= r:
            return 0
        m = (l + r) // 2
        v = new_node(values[m])
        left[v] = build(values, l, m)
        right[v] = build(values, m + 1, r)
        upd(v)
        return v

    def collect(v, out):
        if v == 0:
            return
        collect(left[v], out)
        out.append(val[v])
        collect(right[v], out)

    root = build(list(range(MX)), 0, MX)

    ans = [0] * n
    REBUILD = 5000

    for idx in range(n - 1, -1, -1):
        x = a[idx]
        L, R = split(root, x)
        RL, RR = split(R, x)
        L1, R1 = split(root, MX - x)
        root = merge(RL, L1)
        # find first
        v = root
        while left[v]:
            v = left[v]
        ans[idx] = val[v]

        if (n - 1 - idx) % REBUILD == REBUILD - 1:
            values = []
            collect(root, values)
            # Replace the whole arrays so the old buffers are freed.
            val = [0]
            left = [0]
            right = [0]
            size = [0]
            root = build(values, 0, len(values))

    sys.stdout.write(" ".join(map(str, ans[::-1])))


if __name__ == "__main__":
    solve()
