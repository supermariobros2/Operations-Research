costs = [
    [0, 143, 108, 118, 121, 88, 121, 57, 92],    # home
    [143, 0, 35, 63, 108, 228, 182, 73, 162],    # A
    [108, 35, 0, 45, 86, 193, 165, 42, 129],     # B
    [118, 63, 45, 0, 46, 190, 203, 73, 105],     # C
    [121, 108, 86, 46, 0, 172, 224, 98, 71],     # D
    [88, 228, 193, 190, 172, 0, 174, 160, 108],  # E
    [121, 182, 165, 203, 224, 174, 0, 129, 212], # F
    [57, 73, 42, 73, 98, 160, 129, 0, 117],      # G
    [92, 162, 129, 105, 71, 108, 212, 117, 0]    # H
]

sales = [
    [0.0, 0.0, 0.0], # Home
    [0.3, 0.4, 0.3], # A
    [0.2, 0.5, 0.3], # B
    [0.2, 0.7, 0.1], # C
    [0.3, 0.5, 0.2], # D
    [0.3, 0.6, 0.1], # E
    [0.4, 0.3, 0.3], # F
    [0.0, 0.3, 0.7], # G 
    [0.1, 0.1, 0.8]  # H
]

Cities = range(len(sales))

expected = [500*(0*sales[k][0] + 1*sales[k][1] + 2*sales[k][2]) for k in Cities]


# subtract x from list A
def SSub(A,x):
    return [a for a in A if a != x]

# Contribution function for part (a)
def Ca(t,a):
    return -costs[t][a] + expected[a]

# Value function for part (a)
def TAPa(t,U):
    if len(U) == 4:
        return (-costs[t][0],0)
    else:
        return max((Ca(t,a) + TAPa(a, SSub(U,a))[0],a) for a in U)
    
# Value function for part (b)
def TAPb(t,U,p):
    if (len(U) == 4) or (p == 0):
        return (-costs[t][0],0)
    else:
        return max((-costs[t][a] 
        + sum(sales[a][q]*(500*min(p,q) + TAPb(a, SSub(U,a),p-min(p,q))[0]) for q in range(3)),a)
        for a in U)








