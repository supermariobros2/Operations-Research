from gurobipy import *

# Volume of mail from each post office (m^3)
volume = [111,67,23,67,36,66,49,64,53,41]

# Cost of upgrading to a mail centre ($)
upgrade = [3000,2500,2000,2250,1750,2750,2000,1500,2000,2250]

# Cost rate of moving ($/m^3km)
rate = 1

# Mail centre capacity (m^3)
capacity = 150

# Distance between centres (km)
distance = [
    [0,   67, 51, 38, 21, 42, 56, 31, 59, 34],
    [67, 0,   42, 72, 69, 53, 54, 94, 74, 36],
    [51, 42, 0,   35, 40, 67, 12, 67, 31, 43],
    [38, 72, 35, 0,   17, 74, 31, 37, 23, 55],
    [21, 69, 40, 17, 0,   60, 41, 27, 39, 44],
    [42, 53, 67, 74, 60, 0,   78, 72, 90, 23],
    [56, 54, 12, 31, 41, 78, 0,   67, 20, 54],
    [31, 94, 67, 37, 27, 72, 67, 0,   59, 64],
    [59, 74, 31, 23, 39, 90, 20, 59, 0,   68],
    [34, 36, 43, 55, 44, 23, 54, 64, 68, 0  ],
    ]

P = range(len(volume))

m = Model('Mail')

Y = {p: m.addVar(vtype=GRB.BINARY) for p in P}
X = {(i,j): m.addVar(vtype=GRB.BINARY) for i in P for j in P}

m.setObjective(quicksum(upgrade[p]*Y[p] for p in P)+
               quicksum(rate*distance[i][j]*volume[i]*X[i,j] for i in P for j in P))

for i in P:
    m.addConstr(quicksum(X[i,j] for j in P)==1)
    
for j in P:
    m.addConstr(quicksum(volume[i]*X[i,j] for i in P)<=capacity*Y[j])

m.optimize()

print("Upgrade", [p for p in P if Y[p].x > 0.9])

print("Assign")
for i in P:
    for j in P:
        if X[i,j].x > 0.9:
            print("   ", i, "->", j)

