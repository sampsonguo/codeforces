# Problem: https://codeforces.com/contest/2241/problem/A
#
# Solution:
# 1. Each operation divides the current x by one of its divisors z, so x never increases.
# 2. Therefore the final value y must divide the original x; otherwise it is unreachable.
# 3. If y divides x, we can reach y in one operation by choosing z = x / y.
# 4. So the answer is YES iff x % y == 0.

t = int(input())
for _ in range(t):
    x, y = map(int, input().split())
    print("YES" if x % y == 0 else "NO")
