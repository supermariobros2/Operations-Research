distances = [
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

def Va(t, curr, hist):
    if t == 0:
        return (-distances[curr][0],0)
    return max((expected[i]-distances[curr][i]+Va(t-1,i,hist.union([i]))[0],i)
               for i in Cities if i not in hist)            
            
def Vb(t, curr, hist, nLeft):
    if t==0 or nLeft==0:
        return (-distances[curr][0],0)
    return max((-distances[curr][i]+
               sum(sales[i][n]*(500*min(n,nLeft)+
                   Vb(t-1,i,hist.union([i]),max(nLeft-n,0))[0]) 
                   for n in [0,1,2]), i)
               for i in Cities if i not in hist)           

def Vb2(t, curr, hist, nLeft):
    if t==0 or nLeft==0:
        return (-distances[curr][0],0)
    vList = []
    for i in Cities:
        if i not in hist:
            tSum = 0
            for n in [0,1,2]:
                tSum += sales[i][n]*(500*min(n,nLeft)+\
                        Vb2(t-1,i,hist.union([i]),max(nLeft-n,0))[0])
            vList.append((-distances[curr][i]+tSum, i))
    return max(vList)
            
            
            
    
    
