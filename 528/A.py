

s = raw_input()

ret = ""
while(len(s)>0):
    if len(s) % 2 == 0:
        ret = s[-1] + ret
        s = s[:-1]
    else:
        ret = s[0] + ret
        s = s[1:]

print ret


