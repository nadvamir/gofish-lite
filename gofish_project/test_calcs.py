from math import sqrt, exp

v = 100.0

# testing that the calculations are correct
print "     %4.0f %4.0f %4.0f" % (2.0, 3.0, 4.0)
for b in [1.0, 2.0, 4.0]:
    print "%4.0f" % (b),
    for w in [2.0, 3.0, 4.0]:
        if b == 1.0:
            v = 1000.0
        elif b == 2.0:
            v = 100.0
        else:
            v = 20.0

        df = lambda x: v * exp(-x / b / (w-1))

        s = 0.0; opt = 0
        ratio = 0.0
        for i in range(1, 16):
            s += round(df(i), 0)
            if (s / (b + i) < ratio):
                opt = i - 1
                break
            else:
                ratio = s / (b + i)

        print "%4.0f" % (opt),
    print

