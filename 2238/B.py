# Problem: https://codeforces.com/contest/2238/problem/B
#
# Solution:
# For a prime p, write x=v_p(a), y=v_p(b), z=v_p(c).
# The crimson condition is
#     min(max(x,y), max(y,z)) = min(x,z).
# This holds exactly when y <= min(x,z), i.e. every prime power of b is
# contained in both a and c.  Equivalently, b | gcd(a,c).
#
# So we must count triples (a,b,c) with 1<=a,b,c<=n and b | gcd(a,c).
# Fix b. Then a and c must both be multiples of b, and there are
# floor(n/b) choices for each.  Hence the answer is
#     sum_{b=1}^{n} floor(n/b)^2.

import sys


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for i in range(1, t + 1):
        n = int(data[i])
        ans = 0
        for b in range(1, n + 1):
            k = n // b
            ans += k * k
        out.append(str(ans))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
