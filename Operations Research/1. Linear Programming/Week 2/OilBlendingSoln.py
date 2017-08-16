from gurobipy import *

# Sets
Oils = [0,1,2,3,4]
IsVeg = [True, True, False, False, False]

# Data
Cost = [110, 120, 130, 110, 115]
Hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
MaxVeg = 200
MaxNonVeg = 250
MinHard = 3
MaxHard = 6
SellPrice = 150

m = Model()

# Variables
X = {i: m.addVar() for i in Oils}

# Objective
m.setObjective(quicksum((SellPrice-Cost[i])*X[i] for i in Oils), GRB.MAXIMIZE)

# Constraints
c1 = m.addConstr(quicksum(X[i] for i in Oils if IsVeg[i]) <= MaxVeg)
c2 = m.addConstr(quicksum(X[i] for i in Oils if not IsVeg[i]) <= MaxNonVeg)

c3 = m.addConstr(quicksum((Hardness[i]-MinHard)*X[i] for i in Oils) >= 0)
c4 = m.addConstr(quicksum((Hardness[i]-MaxHard)*X[i] for i in Oils) <= 0)

# Solve it
m.optimize()

# Write out the answer
for i in Oils:
    print(X[i].x)
    
# Write out the slack values for each constraint
print("MaxVeg", c1.slack)
print("MaxNonVeg", c2.slack)
print("MinHard", c3.slack)
print("MaxHard", c4.slack)