from gurobipy import *

# Sets
Oils = [0,1,2,3,4]  #  or range(5)
Veg = [0,1]         # or Oils[:2]
NonVeg = [2,3,4]    # or Oils[2:]
T = range(6)

# Data
Cost = [[110, 130, 110, 120, 100,  90],
        [120, 130, 140, 110, 120, 100],
        [130, 110, 130, 120, 150, 140],
        [110,  90, 100, 120, 110,  80],
        [115, 115,  95, 125, 105, 135]]
Hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
MaxVeg = 200
MaxNonVeg = 250
MinHard = 3
MaxHard = 6
SellPrice = 150
MaxStorage = 1000
StorageCost = 5
StartingLevel = 500

m = Model()

# Variables
X = {(i,t): m.addVar() for i in Oils for t in T}
Y = {(i,t): m.addVar() for i in Oils for t in T}
S = {(i,t): m.addVar(ub=MaxStorage) for i in Oils for t in T}


# Objective
m.setObjective( quicksum(SellPrice*X[i,t] for i in Oils for t in T)-
                quicksum(Cost[i][t]*Y[i,t] for i in Oils for t in T)-
                quicksum(StorageCost*S[i,t] for i in Oils for t in T), GRB.MAXIMIZE)

# Constraints
for t in T:
    m.addConstr(quicksum(X[i,t] for i in Veg)<=MaxVeg)
    m.addConstr(quicksum(X[i,t] for i in NonVeg)<=MaxNonVeg)
    m.addConstr(quicksum((Hardness[i]-MinHard)*X[i,t] for i in Oils)>=0)
    m.addConstr(quicksum((Hardness[i]-MaxHard)*X[i,t] for i in Oils)<=0)
    if t > 0:
        for i in Oils:
            m.addConstr(S[i,t]==S[i,t-1]+Y[i,t]-X[i,t])

for i in Oils:
    m.addConstr(S[i,0]==StartingLevel+Y[i,0]-X[i,0])
    # End with at least as much as we started with
    m.addConstr(S[i,T[-1]]>=StartingLevel)
            
# Solve it
m.optimize()

# Write out the answer
print('Refining')
for i in Oils:
    print([round(X[i,t].x,2) for t in T])
print('Purchases')
for i in Oils:
    print([round(Y[i,t].x,2) for t in T])
print('Storage')
for i in Oils:
    print([round(S[i,t].x,2) for t in T])
    
    
    
    
    