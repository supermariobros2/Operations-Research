from gurobipy import *

"""
Forgot storage limit constraint.
All good though. Finish part two.

Solution:
$93711.5 - need to validate based on solution script (incomplete)

ii)
Fixed maintenance schedule can now be adjusted to maintain as you desire.

Solution:
$108855 - well done - but non-unique maintenance schedule

"""

# Set up your own data
profit = [10, 6, 8, 4, 11, 9, 3]
P = range(len(profit)) # no. of products (7)

n = [4, 2, 3, 1, 1] # no. of each type of machine
M = range(len(n)) # 5 types of machines

# usage[P][M]
usage = [ # production time per machine (hours)
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

# formulation continued

StorageLimit = 100 # of each product
StorageCost = 0.5 # $/unit/month
FinalStock = 50 # for each product at the end of June
MonthlyHours = 16*24 # factory works for 16 hours a day for 24 days a month (and with no sequencing problems)

model = Model("Factory Production")

# Variables

# produced
X = {(t,p): model.addVar(vtype = GRB.INTEGER) for t in T for p in P}
# sold
Y = {(t,p): model.addVar(vtype = GRB.INTEGER, ub = market[p][t]) for t in T for p in P}
# stored
S = {(t,p): model.addVar(vtype = GRB.INTEGER, ub = StorageLimit) for t in T for p in P}
# maintenance schedule
Ma = {(t,m): model.addVar(vtype = GRB.INTEGER) for t in T for m in M}


# Objective
model.setObjective(quicksum(Y[t,p]*profit[p] - S[t,p]*StorageCost for t in T for p in P), GRB.MAXIMIZE)

# Constraints

    # production
for t in T:
    # machine usage
    for m in M:
        model.addConstr(quicksum(usage[p][m]*X[t,p] for p in P) <= (n[m] - Ma[t,m])*MonthlyHours) # modified for flexi-maintenance

    # storage
    if t == 0:
        for p in P:
            model.addConstr(S[t,p] == X[t,p] - Y[t,p])
    else:
        for p in P:
            model.addConstr(S[t,p] == S[t-1,p] + X[t,p] - Y[t,p])

    # Final storage value additional constraint
    if t == T[-1]:
        for p in P:
            model.addConstr(S[t,p] == FinalStock)

    # maintenance constraints
    for m in M:
        model.addConstr(quicksum(Ma[t,m] for t in T) == quicksum(maint[t][m] for t in T))

    # model.addConstr(quicksum(Ma[t,m] for m in M)<=2) # extra constraint thrown in - doesn't impact optimality

# Solution
model.optimize()

print "Solution:"

print "\nProduction:"
for p in P:
    print p, [int(X[t,p].x) for t in T]

print "\nSold:"
for p in P:
    print p, [int(Y[t,p].x) for t in T]

print "\nStored:"
for p in P:
    print p, [int(S[t,p].x) for t in T]

print "\nMaintenance:"
for m in M:
    print m, [int(Ma[t,m].x) for t in T]


# for t in T:
#     print "Month", t+1
#     print "Produced:", [X[t,p].x for p in P]
#     print "Sold:", [Y[t,p].x for p in P]
#     print "Stored:", [S[t,p].x for p in P]
#     print "Maintenance:", [Ma[t,m].x for m in M]

# check market limit was met
for t in T:
    for p in P:
        if Y[t,p].x > market[p][t]: print "Solution is wrong"




