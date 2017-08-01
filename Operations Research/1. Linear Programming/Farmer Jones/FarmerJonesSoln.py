from gurobipy import *

m = Model()

# Sets
Cakes = ["Chocolate","Plain"]
Ingredients = ["Eggs","Milk","BakingTime"]

C = range(len(Cakes))
I = range(len(Ingredients))

# Data
price = [4, 2]
available = [30,5,480]
usage = [
         [4,1],
         [0.25,0.2],
         [20,50]
         ]

         
# Variables
X = {}
for c in C:
    X[c] = m.addVar()
    
# Objective
m.setObjective(quicksum(price[c]*X[c] for c in C), GRB.MAXIMIZE)

# Constraints
for i in I:
    m.addConstr(quicksum(usage[i][c]*X[c] for c in C) <= available[i])


m.optimize()

for c in C:
    print(Cakes[c]," = ",X[c].x)
    
    
    
    