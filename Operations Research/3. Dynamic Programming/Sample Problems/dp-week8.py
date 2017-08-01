def Fact1(n):
    Total = 1
    while n > 1:
        Total *= n
        n -= 1
    return Total

# The factorial function is naturally defined recursively

def Fact2(n):
    return n*Fact(n-1) if n > 1 else 1    
    
def Fact(n):
    if n > 1:
        return n*Fact(n-1)
    else:
        return 1

# DP2 Knapsack Alternative

V = [7,4,3]
T = [25,12,8]
J = range(3)
minV = min(V)

_DP2 = {}
def DP2(w):
    if w < minV:
        return 0
    else:
        if w not in _DP2:
            _DP2[w] = max(T[j]+DP2(w-V[j]) for j in J if V[j]<=w)
        return _DP2[w]

# The Fibonacci function illustrates the need for memoisation

_Fib = {}
def Fib(n):
    if n <= 2:
        return 1
    else:
        if n not in _Fib:
            _Fib[n] = Fib(n-1)+Fib(n-2)
        return _Fib[n]


# DP9 Minimal Studying

Sub = range(3)
Pass = [
    [0.20, 0.25, 0.10],
    [0.30, 0.30, 0.30],
    [0.35, 0.33, 0.40],
    [0.38, 0.35, 0.45],
    [0.40, 0.38, 0.50]]

# Minimise the probability of failing all remaining subjects     

def DP9(hr, sub):
    if sub==0:
        return (1,0, 0)
    return min(((1-Pass[x][sub-1])*DP9(hr-x,sub-1)[0], x, hr-x)
                    for x in range(hr+1))
    
def DP9Answer():
    hr = 4
    for s in reversed(Sub):
        retval = DP9(hr,s+1)
        hr = retval[2]
        print('Subject', s+1, 'Hours', retval[1])
    
    
    
