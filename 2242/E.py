# Problem: https://codeforces.com/contest/2242/problem/E
#
# Solution sketch:
# C(x) is periodic with period len(x).  Position p of C(x) is 1 iff
# the bit at offset (p mod len(x)) in x's binary representation is 1.
# The product C(x) & C(y) is 1 at p iff both C(x)[p] and C(y)[p] are 1.
#
# We enumerate a small candidate set of numbers in [l, r] that is rich enough
# to contain the optimal pair:
#   - l and r themselves
#   - for each bit boundary i, the numbers just below/above the boundary
#     (l with lower i bits set to 1, r with lower i bits cleared, and their
#     +/-1 neighbours)
#   - for each binary length present in [l, r], the best possible product of
#     two numbers of that length (which is the closure of the AND of the
#     whole length-L sub-interval).
# Then we try all pairs of candidate numbers, keep the lexicographically
# smallest product (compared as integers of the same length n).

import sys


def closure_mask(x, n):
    """Return an n-bit integer whose binary representation is the first n
    symbols of C(x)."""
    s = bin(x)[2:]
    L = len(s)
    # repeat s enough times and take the lowest n bits
    repeated = s * ((n // L) + 2)
    return int(repeated[:n], 2)


def range_and(lo, hi):
    """Bitwise AND of all integers in [lo, hi]."""
    d = lo ^ hi
    if d == 0:
        return lo
    mask = -1 << d.bit_length()
    return lo & mask


def candidate_numbers(l, r):
    cands = {l, r}
    for i in range(31):
        mask = (1 << i) - 1
        a = l | mask
        if l <= a <= r:
            cands.add(a)
        if l <= a + 1 <= r:
            cands.add(a + 1)
        b = r & ~mask
        if l <= b <= r:
            cands.add(b)
        if l <= b - 1 <= r:
            cands.add(b - 1)
    return sorted(cands)


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    p = 1
    for _ in range(t):
        l = int(data[p])
        r = int(data[p + 1])
        n = int(data[p + 2])
        p += 3

        cands = candidate_numbers(l, r)
        masks = [closure_mask(x, n) for x in cands]

        best = None

        # pairs of candidates with different (or same) lengths
        m = len(cands)
        for i in range(m):
            mx = masks[i]
            for j in range(i + 1, m):
                val = mx & masks[j]
                if best is None or val < best:
                    best = val

        # same-length optimal: for each length L, AND of the whole sub-interval
        for L in range(1, 31):
            lo = max(l, 1 << (L - 1))
            hi = min(r, (1 << L) - 1)
            if lo >= hi:
                continue
            v = range_and(lo, hi)
            val = closure_mask(v, n)
            if best is None or val < best:
                best = val

        out.append(format(best, f"0{n}b"))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
