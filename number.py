def stringified(i):
    t = ""
    if i < 1000: return str(i)
    if i > 999 and i < 1000000:
        t = str(round(i/1000, 1)) + "k"
    if i > 999999 and i < 1000000000:
        t = str(round(i/1000000, 1)) + "m"
    if i > 999999999 and i < 1000000000000:
        t = str(round(i/1000000000, 1)) + "b"
    if i >= 1000000000000 and i < 1000000000000000:
        t = str(round(i/1000000000000, 1)) + "t"
    t = t.replace(".0", "")
    if t != "": return t
    c = 0
    while i > 10:
        i = round(i / 10, 1)
        c += 1
    return str(i) + "*10^" + str(c)
