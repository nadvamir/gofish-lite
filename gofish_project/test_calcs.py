from math import *
import matplotlib.pyplot as plt

# showing how many times to fish is optimal
vals = [20, 80, 200, 800]
boats = [8.0, 8.0, 4.0, 2.0]
times = [
    [4, 8, 12],
    [4, 8, 12],
    [3, 6, 9],
    [2, 4, 5]
]

for i in range(4):
    v = vals[i]
    b = boats[i]
    for j in range(3):
        n = times[i][j]
        beta = n / (b + n)

        print "%4.2f" % (beta),

        g  = lambda x: v * pow(x, beta)
        dg = lambda x: g(x) - g(x-1)
        df = lambda x: v * beta * pow(x, beta - 1)

        xs = range(1, 20 + int(b))
        ss = [0] * int(b)
        s = 0.0; opt = 0
        ratio = 0.0
        for k in range(1, 20):
            s += round(dg(k))
            ss.append(s)
#            print "%4.4f" % (s/(b+k)),
            if (s / (b + k) < ratio):
                opt = k - 1
                break
            else:
                ratio = s / (b + k)

        print "%4.0f" % (opt),#, "%4.4f" % (s), "%4.4f" % dg(1),
    print
        
