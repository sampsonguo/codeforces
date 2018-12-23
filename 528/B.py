

n, k = map(int, raw_input().strip().split())

min_x = -1

for i in range(1, k):
    if n % i == 0:
        a = i
        b = n/i
        x = a + b*k
        if min_x == -1:
            min_x = x
        else:
            min_x = min(x, min_x)

print min_x
