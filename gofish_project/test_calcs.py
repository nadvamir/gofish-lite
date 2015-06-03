from math import sqrt, exp

v = 100.0

# showing how many times to fish is optimal
# bs -- boats, i.e. moving cost (1 == fishing cost)
# ws -- weathers, the larger -- the longer to sit in one spot
def printTests(bs, ws):
    print "b/w %4.0f %4.0f %4.0f" % (ws[0], ws[1], ws[2])
    for i in range(len(bs)):
        b = bs[i]
        v = 20 + 10 ^ (i+1)

        print "%3.0f" % (b),

        for w in ws:
            #df = lambda x: v * exp(-x / b / (w-1))
            df = lambda x: v * exp(-2 * x / b / (w - 2))

            s = 0.0; opt = 0
            ratio = 0.0
            for i in range(1, 50):
                s += round(df(i), 0)
                if (s / (b + i) < ratio):
                    opt = i - 1
                    break
                else:
                    ratio = s / (b + i)

            print "%4.0f" % (opt),
        print
    print

printTests([2.0, 4.0, 8.0], [2.5, 3.0, 4.0])
printTests([2.0, 4.0, 8.0], [2.5, 3.5, 5.0]) # this one seems reasonable
printTests([2.0, 6.0, 12.0], [2.5, 4.0, 6.0])
printTests([2.0, 4.0, 8.0], [2.5, 3.8, 5.5])
printTests([2.0, 4.0, 6.0], [2.5, 3.0, 4.0])
printTests([2.0, 4.0, 8.0], [2.5, 4.0, 6.0])
