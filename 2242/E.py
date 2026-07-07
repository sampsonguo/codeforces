# Problem: https://codeforces.com/contest/2242/problem/E
#
# Solution sketch:
# C(x) is periodic with period len(x).  Position p of C(x) is 1 iff
# the bit at offset (p mod len(x)) in x's binary representation is 1.
# The product C(x) & C(y) is 1 at p iff both C(x)[p] and C(y)[p] are 1.
#
# We enumerate a small candidate set of numbers in [l, r] that is rich enough
# to contain the optimal cross-length pair:
#   - l and r themselves
#   - for each of the largest binary lengths present in [l, r], the smallest
#     and largest numbers of that length, the power of two of that length
#     (if it lies in the interval), and their immediate neighbours.
# The best same-length pair is handled separately: for each length L, the
# closure of the AND of the whole length-L sub-interval is a candidate.
# Then we try all pairs, keep the lexicographically smallest product
# (compared as integers of the same length n).

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


def candidate_numbers(l, r, top_k=8):
    """Return a small sorted list of candidate numbers in [l, r].

    Only the largest few binary lengths are considered for cross-length pairs,
    because a longer period tends to push the first common '1' further to the
    right, which is what lexicographic minimisation wants.  The best same-length
    pair is handled separately.
    """
    lengths = []
    for L in range(1, 31):
        lo = max(l, 1 << (L - 1))
        hi = min(r, (1 << L) - 1)
        if lo < hi:
            lengths.append((L, lo, hi))
    # longest lengths first
    lengths.sort(reverse=True)

    cands = {l, r}
    for L, lo, hi in lengths[:top_k]:
        cands.add(lo)
        cands.add(hi)
        p = 1 << (L - 1)
        if l <= p <= r:
            cands.add(p)
        if lo + 1 <= hi:
            cands.add(lo + 1)
        if hi - 1 >= lo:
            cands.add(hi - 1)
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
