from gurobipy import *

"""
Optimise a portfolio given certain constraints. Maximise returns while limiting high-risk exposure.

Solution:
$9542.14

Sanity check Objective and other constraints:
- best return is 12.7% - $12,700 is max before any constraints
- 40000 in USA
- 30000 in computers
- 20000 in appliances
- 20000 in insurance
- 25000 in bonds
- STBonds are 40% of MTBonds
- all add up to $100,000

- solution appears correct

"""

model = Model("Portfolio Optimisation")

# # Sets - should really be a class - also zero-indexing - class/dictionary sorts this out

# FinancialProducts = range(10)
# Type = ["Cars", "Cars", "Computers", "Computers", "Appliances", "Appliances", "Insurance", "Insurance", "Bonds", "Bonds"]
# Country = ["Germany", "Japan", "USA", "Singapore", "Europe", "Asia", "Germany", "USA", None, None]

# # Data

# F = FinancialProducts

# Returns = [10.3, 10.1, 11.8, 11.4, 12.7, 12.2, 9.5, 9.9, 3.6, 4.2]

# FundLimit = 100000 # $equity
# STBonds = 8
# MTBonds = 9

# # data constraints
# CarMax = 30000
# ComputerMax = 30000
# ApplianceMax = 20000
# InsuranceMin = 20000
# BondsMin = 25000
# ShortPCMediumMin = 0.4 # 40%
# GermanyMax = 50000
# USAMax = 40000

# # Variables
# X = {f: model.addVar() for f in F}

# # Objective

# model.setObjective(quicksum(Returns[f]/100.*X[f] for f in F),GRB.MAXIMIZE)

# # Constraints
# c0 = model.addConstr(quicksum(X[f] for f in F) <= FundLimit)
# c1 = model.addConstr(quicksum(X[f] for f in F if Type[f] == "Cars") <= CarMax)
# c2 = model.addConstr(quicksum(X[f] for f in F if Type[f] == "Computers") <= ComputerMax)
# c3 = model.addConstr(quicksum(X[f] for f in F if Type[f] == "Appliances") <= ApplianceMax)
# c4 = model.addConstr(quicksum(X[f] for f in F if Type[f] == "Insurance") >= InsuranceMin)
# c5 = model.addConstr(quicksum(X[f] for f in F if Type[f] == "Bonds") >= BondsMin)
# c6 = model.addConstr(X[MTBonds]*ShortPCMediumMin <= X[STBonds])
# c7 = model.addConstr(quicksum(X[f] for f in F if Country[f] == "Germany") <= GermanyMax)
# c8 = model.addConstr(quicksum(X[f] for f in F if Country[f] == "USA") <= USAMax)



# # Solution

# model.optimize()

# for f in F:
# 	print F[f]+1, Type[f], Country[f], '=', X[f].x
# 	print "Return:", X[f].x*Returns[f]/100.


### Now let's do it as a dictionary - class?
P = { # printing returns the dictionary key (in this case: 1, 2, 3, ..., 10)
    1: (10.3, "Cars (Germany)"),
    2: (10.1, "Cars (Japan)"),
    3: (11.8, "Computers (USA)"),
    4: (11.4, "Computers (Singapore)"),
    5: (12.7, "Appliances (Europe)"),
    6: (12.2, "Appliances (Asia)"),
    7: ( 9.5, "Insurance (Germany)"),
    8: ( 9.9, "Insurance (USA)"),
    9: ( 3.6, "Short-term bonds"),
    10:( 4.2, "Medium-term bonds")
}

# Variables
X = {p: model.addVar() for p in P}

# Objective
model.setObjective(quicksum(X[p]*P[p][0]/100 for p in P),GRB.MAXIMIZE)

# Constraints
model.addConstr(quicksum(X[p] for p in P) <= 100000)

C = {}
C["Cars"] = model.addConstr(X[1] + X[2] <= 30000)
C["Computers"] = model.addConstr(X[3] + X[4] <= 30000)
C["Appliances"] = model.addConstr(X[5] + X[6] <= 20000)
C["Insurance"] = model.addConstr(X[7] + X[8] >= 20000)
C["Bonds"] = model.addConstr(X[9] + X[10] >= 25000)
C["Short/Medium"] = model.addConstr(X[10]*0.4 <= X[9])
C["Germany"] = model.addConstr(X[1] + X[7] <= 50000)
C["USA"] = model.addConstr(X[3] + X[8] <= 40000)

# solution
model.optimize()

print '\n', "Portfolio is"
for p in P:
    if X[p].x > 0:
        print(P[p][1], round(X[p].x,2))     

print '\n',"Return is", model.objVal
for p in P:
    print(P[p][1], round(X[p].rc,4), round(X[p].x,2), 
          round(X[p].SAObjLow,4), round(X[p].Obj,4), round(X[p].SAObjUp,4))     

print '\n', "Slacks and Shadow Prices"
for k in C:
    print(k, C[k].Slack, round(C[k].pi,3), 
          round(C[k].SARHSLow,2), C[k].RHS, round(C[k].SARHSUp,2))