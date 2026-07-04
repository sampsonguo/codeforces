# Problem: https://codeforces.com/contest/2241/problem/F
#
# Solution:
# A position is losing for the player to move (a P-position) iff
# every "10" boundary in the string is flanked by even-length runs,
# i.e. the block of consecutive '1's before the boundary has even length
# AND the block of consecutive '0's after the boundary has even length.
#
# Why this is true:
#
# 1. An odd-inversion subsequence must contain at least one '1' before a '0'.
#    The simplest example is "10" (one inversion). More generally, a
#    subsequence consisting of k 1's followed by m 0's has k*m inversions,
#    which is odd iff both k and m are odd.
#
# 2. Therefore a move can be viewed as removing some 1's and 0's across
#    "10" boundaries. Removing an odd number of 1's and an odd number of
#    0's from a single "10" boundary flips the parities of both adjacent
#    run lengths.
#
# 3. Reduce the string by keeping only the parity of each maximal run:
#    an even-length run disappears, an odd-length run becomes a single
#    character. The reduced string contains a "10" boundary exactly when
#    the original string has a "10" boundary whose two adjacent runs are
#    not both even.
#
# 4. Positions whose reduced string has no "10" boundary (i.e. it looks
#    like 0...01...1 or is empty) are precisely the P-positions: every
#    legal move touches a "10" boundary and therefore creates an odd
#    run in the reduced string, leaving the opponent a winning reply.
#
# In particular, sorted strings like 0...01...1 contain no "10" boundary,
# so they are losing; strings like 1100, 110000, 111100, 0...01100...1
# are losing because each "10" boundary has even runs.

import sys


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx])
        idx += 1
        s = data[idx].decode()
        idx += 1

        bob_wins = True
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            # If this run is '1's and is followed by '0's, check the boundary.
            if s[i] == "1" and j < n and s[j] == "0":
                ones_len = j - i
                k = j
                while k < n and s[k] == "0":
                    k += 1
                zeros_len = k - j
                if ones_len % 2 == 1 or zeros_len % 2 == 1:
                    bob_wins = False
                    break
            i = j

        out.append("Bob" if bob_wins else "Alice")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
