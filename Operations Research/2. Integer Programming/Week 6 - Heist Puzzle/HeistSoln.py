from gurobipy import *

S = range(16)
P = range(4)
SquaresUsed = [
    [[4,8,12,13],[9,10,11,13],[2,3,7,11],[7,9,10,11],[10,12,13,14]],
    [[2,6,9,10],[4,8,9,10],[0,1,4,8],[2,3,6,10],[0,1,2,6],[8,9,10,14]],
    [[0,1,4,5],[1,2,5,6],[5,6,9,10],[4,5,8,9]],
    [[3,7,11,15],[12,13,14,15]]
]

Placements = [range(len(SquaresUsed[p])) for p in P]

m = Model('Heist')

X = {(p,i): m.addVar(vtype=GRB.BINARY) for p in P for i in Placements[p]}

for p in P:
    m.addConstr(quicksum(X[p,i] for i in Placements[p])==1)

for s in S:
    m.addConstr(quicksum(X[p,i] for p in P for i in Placements[p]
                         if s in SquaresUsed[p][i])==1)

m.setParam('OutputFlag',0)

while True:
    m.optimize()
    if m.status==GRB.INFEASIBLE:
        break
    
    for p in P:
        for i in Placements[p]:
            if X[p,i].x > 0.99:
                print (p, i, SquaresUsed[p][i])
    print("")
    m.addConstr(quicksum(X[p,i] for p in P for i in Placements[p]
                         if X[p,i].x > 0.99)<=3)
    
    