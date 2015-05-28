from random import uniform

#################################################################
# HELPERS
#################################################################
# positive(val) returns val if it is positive
# 0 otherwise. 
def positive(val):
    return val if val > 0 else 0.0

# nth returns a reduced value for every n times, 0 otherwise
def nth(i, n, val, red):
    return positive(val - i/n*red) if (i + 1) % n == 0 else 0.0

#################################################################
# NEW-STYLE YIELDS
#################################################################
def makeUniformDecliningYield(n, options):
    zeroAt = options['zero-at']
    reduction = 1.0 / zeroAt
    return [positive(1.0 - i * reduction) for i in range(n)]

def makeUniformConstantYield(n, options):
    val = options['val']
    return [val for i in range(n)]

def makeUniformRandomYield(n, options):
    lower = options['lower']; upper = options['upper']
    return [uniform(lower, upper) for i in range(n)]

def makeNthDecliningYield(n, options):
    everyN = options['n']; zeroAtN = options['zero-at-n']
    reduction = 1.0 / zeroAtN
    return [nth(i, everyN, 1.0, reduction) for i in range(n)]

def makeNthConstantYield(n, options):
    everyN = options['n']; val = options['val']
    return [nth(i, everyN, val, 0.0) for i in range(n)]

