from gurobipy import *

# Set up your own data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit))

n = [4, 2, 3, 1, 1]
M = range(len(n))

# usage[P][M]
usage = [
    [0.5, 0.1, 0.2, 0.05, 0.00],
    [0.7, 0.2, 0.0, 0.03, 0.00],
    [0.0, 0.0, 0.8, 0.00, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.00],
    [0.3, 0.0, 0.0, 0.10, 0.05],
    [0.2, 0.6, 0.0, 0.00, 0.00],
    [0.5, 0.0, 0.6, 0.08, 0.05]
    ]

T = range(6)

# maintenance[T][M]
maint = [
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1]
    ]

# market[P][T]
market = [
    [ 500, 600, 300, 200,   0, 500],
    [1000, 500, 600, 300, 100, 500],
    [ 300, 200,   0, 400, 500, 100],
    [ 300,   0,   0, 500, 100, 300],
    [ 800, 400, 500, 200,1000,1100],
    [ 200, 300, 400,   0, 300, 500],
    [ 100, 150, 100, 100,   0,  60]
    ]

MaxStore = 100
StoreCost = 0.5
FinalStore = 50
MonthHours = 16*24

m = Model('Factory Planning')

# Dictionary comprehension
X = {(p,t): m.addVar(vtype=GRB.INTEGER, ub=market[p][t]) for p in P for t in T}
Y = {(p,t): m.addVar(vtype=GRB.INTEGER) for p in P for t in T}
S = {(p,t): m.addVar(vtype=GRB.INTEGER, ub=MaxStore) for p in P for t in T}
Z = {(t,i): m.addVar(vtype=GRB.INTEGER) for t in T for i in M}

m.setObjective(quicksum(profit[p]*X[p,t] for p in P for t in T)-
               quicksum(StoreCost*S[p,t] for p in P for t in T),GRB.MAXIMIZE)     

for i in M:
    m.addConstr(quicksum(Z[t,i] for t in T)==
                quicksum(maint[t][i] for t in T))
    for t in T:
        m.addConstr(quicksum(usage[p][i]*Y[p,t] for p in P)<=
                    (n[i]-Z[t,i])*MonthHours)
        
for p in P:
    S[p,-1] = 0
    m.addConstr(S[p,T[-1]]>=FinalStore)
    for t in T:
        m.addConstr(S[p,t]==S[p,t-1]+Y[p,t]-X[p,t])
        
for t in T:
    m.addConstr(quicksum(Z[t,i] for i in M)<=2)

m.optimize()

print('\nSales')
for p in P:
    print(p, [int(X[p,t].x) for t in T])

print('\nProduction')
for p in P:
    print(p, [int(Y[p,t].x) for t in T])

print('\nStorage')
for p in P:
    print(p, [int(S[p,t].x) for t in T])
    
print('\nMaintenance')
for i in M:
    print(i, [int(Z[t,i].x) for t in T])

