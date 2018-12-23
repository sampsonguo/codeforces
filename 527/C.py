
n = int(input())

L = []
cnt = {}

LI = []

for i in range(n*2-2):
    LI.append(raw_input())
    cnt.setdefault(LI[i][0], 0)
    cnt[LI[i][0]] += 1

L = sorted(LI, key = lambda x: len(x), reverse=True)


S = ""

if L[0][1:] == L[1][:-1] and cnt[L[0][0]] >= n-1:
    S = L[0] + L[1][-1]
else:
    S = L[1] + L[0][-1]


flag = [0] * (n+1)

ret = ""
for i in range(n*2-2):
    if S[:len(LI[i])] == LI[i] and flag[len(LI[i])] == 0:
        ret += "P"
        flag[len(LI[i])] = 1
    else:
        ret += "S"

print ret
