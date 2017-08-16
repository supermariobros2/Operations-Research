from gurobipy import *

# Set up the data as a dictionary (so indices match the labels in the problem)
P = {
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

# Create the Model object
m = Model("Portfolio")

# Create all your variables
X = {p:m.addVar() for p in P}

m.setObjective(quicksum(P[p][0]/100*X[p] for p in P), GRB.MAXIMIZE) 

m.addConstr(quicksum(X[p] for p in P)<=100000)  

C = {}
C["Cars"]       = m.addConstr(X[1]+X[2]<=30000) 
C["Computers"]  = m.addConstr(X[3]+X[4]<=30000) 
C["Appliances"] = m.addConstr(X[5]+X[6]<=20000) 
C["Insurance"]  = m.addConstr(X[7]+X[8]>=20000) 
C["Bonds"]      = m.addConstr(X[9]+X[10]>=25000) 
C["Short/Medium"] = m.addConstr(X[9]>=0.4*X[10]) 
C["Germany"]    = m.addConstr(X[1]+X[7]<=50000) 
C["USA"]        = m.addConstr(X[3]+X[8]<=40000) 

m.optimize()     

print("\nPortfolio is")
for p in P:
    if X[p].x > 0:
        print(P[p][1], round(X[p].x,2))     

print("\nReturn is", m.objVal)
for p in P:
    print(P[p][1], round(X[p].rc,4), round(X[p].x,2), 
          round(X[p].SAObjLow,4), round(X[p].Obj,4), round(X[p].SAObjUp,4))     

print("\nSlacks and Shadow Prices")
for k in C:
    print(k, C[k].Slack, round(C[k].pi,3), 
          round(C[k].SARHSLow,2), C[k].RHS, round(C[k].SARHSUp,2))

