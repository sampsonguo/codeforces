

ax, ay = map(int, raw_input().split())
bx, by = map(int, raw_input().split())
cx, cy = map(int, raw_input().split())

if ax > bx:
    ax, bx = bx, ax
    ay, by = by, ay
if bx > cx:
    bx, cx = cx, bx
    by, cy = cy, by
if ax > bx:
    ax, bx = bx, ax
    ay, by = by, ay

ret = []
for i in range(min(ay, by, cy), max(ay, by, cy)+1):
    ret.append([bx, i])

for i in range(ax, bx):
    ret.append([i, ay])

for i in range(bx+1, cx+1):
    ret.append([i, cy])

print len(ret)
for i in range(len(ret)):
    print("%d %d"%(ret[i][0], ret[i][1]))


