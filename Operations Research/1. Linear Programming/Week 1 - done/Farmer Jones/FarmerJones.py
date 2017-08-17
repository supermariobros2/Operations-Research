from gurobipy import *

# Farmer Jones problem. Slightly oversimplified in that fractional cakes can be produced

# solution is $37.33 profit making and selling 5.67 chocolate cakes and 7.33 plain cakes

# m = Model()

# x1 = m.addVar()
# x2 = m.addVar()

# m.setObjective(4*x1+2*x2,GRB.MAXIMIZE)

# m.addConstr(20*x1+50*x2<=8*60)
# m.addConstr(250*x1+200*x2<=5*1000)
# m.addConstr(4*x1+x2<=30)

# m.optimize()


# a more formal (and generalised layout)

m = Model()

# Sets

Cakes = ["Chocolate","Plain"]
Ingredients = ["Baking Time","Milk","Eggs"]

C = range(len(Cakes)) # range is used for iterating from 0 through to the length - 1
I = range(len(Ingredients))

# Data
price = [4,2]
available = [8*60,5*1000,30]
usage = [
		[20,50],
		[250,200],
		[4,1]
		]

# Variables
X = {}
for c in C:
	X[c] = m.addVar()

# Objective
m.setObjective(quicksum(price[c]*X[c] for c in C),GRB.MAXIMIZE)
# quicksum is a gurobi version of the sum function which is much faster than sum and useful for generating large expressions
# N.B. it is still inferior to addTerms or the LinExpr() constructor - dunno what that is yet

# Constraints
Y = {} # initialise
for i in I:
	Y[i] = m.addConstr(quicksum(usage[i][c]*X[c] for c in C) <= available[i])

m.optimize()

for c in C:
    print(Cakes[c]," = ",X[c].x) # variable.x will give the optimal value for that variable