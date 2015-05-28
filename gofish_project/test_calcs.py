from math import sqrt, exp

v = 100.0

# testing that the calculations are correct
for b in [1.0, 2.0, 4.0]:
    for w in [2.0, 3.0, 4.0]:

        df = lambda x: v * exp(-x / b / (w-1))

        print '---------------------------'
        print 'predicted: ', w*b - b

        s = 0.0
        for i in range(1, 16):
            s += df(i)
            print i, s, df(i), (s/(b+i))

