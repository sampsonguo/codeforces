# Problem: https://codeforces.com/contest/2242/problem/C
#
# Solution:
# The original array is sorted, so group equal numbers and keep only the
# group sizes c_1, c_2, ..., c_m.
#
# In one operation every currently existing group is either increased by 1
# (duplicate) or decreased by 1 (delete), all groups at the same time.
# Therefore the differences between alive group sizes never change.
# A group disappears exactly when its size hits 0.
#
# Consequently the final alive groups are precisely those whose initial size
# is at least some threshold s. Let S = {i | c_i >= s}, m = |S|,
# C = sum_{i in S} (c_i - s). If the smallest final group size is b (b >= 1),
# then the total length is
#       k = C + m * b.
#
# For every distinct initial group size s we check whether this equation has
# an integer solution b >= 1.

import sys


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        k = int(data[idx + 1])
        idx += 2
        a = list(map(int, data[idx : idx + n]))
        idx += n

        # group sizes of equal values
        counts = []
        i = 0
        while i < n:
            j = i
            while j < n and a[j] == a[i]:
                j += 1
            counts.append(j - i)
            i = j

        counts.sort()
        m = len(counts)

        # suffix sums of sorted counts
        suffix_sum = [0] * (m + 1)
        for p in range(m - 1, -1, -1):
            suffix_sum[p] = suffix_sum[p + 1] + counts[p]

        ans = 0
        pos = 0
        prev_s = -1
        for s in counts:
            if s == prev_s:
                continue
            while pos < m and counts[pos] < s:
                pos += 1
            size = m - pos
            total = suffix_sum[pos]
            C = total - size * s
            # need k = C + size * b with b >= 1
            if k >= C + size and (k - C) % size == 0:
                ans += 1
            prev_s = s

        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
