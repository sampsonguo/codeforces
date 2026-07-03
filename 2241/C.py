# Problem: https://codeforces.com/contest/2241/problem/C
#
# Solution:
# The answer is 2 only when the string is already "sorted" and contains
# both characters, i.e. it looks like 000...111... or 111...000...
# In that case every palindromic substring lies completely inside one of
# the two uniform blocks, so we can only shrink each block down to one
# character and get stuck at length 2 ("01" or "10").
# Otherwise the string contains both a "01" boundary and a "10" boundary,
# which creates a palindrome like "010" or "101" crossing the boundary,
# allowing us to reduce the string to length 1.

import sys


def solve():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        s = data[idx]
        idx += 1
        if len(set(s)) == 1:
            out.append("1")
        elif ("01" in s) and ("10" in s):
            out.append("1")
        else:
            out.append("2")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
