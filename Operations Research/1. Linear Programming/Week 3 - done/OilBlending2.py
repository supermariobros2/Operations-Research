from gurobipy import *

"""
Refinement of raw oils and blending optimally (per tonne).
2 types of vege oils are made and 3 types of non-vege oils.

2nd version of the problem is modified so that one can buy oils on the futures market and store for a cost.
At most 1000 tonnes of each oil can be stored and a contingency stock of 500 should always be maintained (I put that in)


Solution:
$102,481.48 - made assumption that storage level always had to be >=500 -> actually $55,351.85 after fixing error

Correct:
$107,842.59

Pretty damn interesting. Only buy in months when it's cheap and basically two production regimes.
Let's have a look at removing that last inventory limit. Only buy 200 tonnes of veg 1 in the very last month.
Everything gets used up and you make $358,250.00. Considering the final stored value for June is $272,500 - difference between profits is: $250,407.41



"""

model = Model()

# Sets

Oils = ["Veg 1", "Veg 2", "Oil 1", "Oil 2", "Oil 3"]
IsVeg = [True, True, False, False, False]

Months = ["January", "February", "March", "April", "May", "June"]

# Data

Hardness = [8.8,6.1,2.0,4.2,5.0] # some unit
ProductionLimits = [200,250] # tonnes of vege oil and non-vege oil respectively
HardnessLimits = [3,6] # lower and upper bounds
SellPrice = 150 # $/tonne

MaxStorage = 1000
StorageCost = 5
StartingLevel = 500

BuyPrice = [ # oils x months # $/tonne 
			[110, 130, 110, 120, 100,  90], # note: indexed via BuyPrice[i][j] (i.e. not by tuple)
        	[120, 130, 140, 110, 120, 100],
        	[130, 110, 130, 120, 150, 140],
        	[110,  90, 100, 120, 110,  80],
        	[115, 115,  95, 125, 105, 135],
			]

O = range(len(Oils))
M = range(len(Months))
Veg = 0
NonVeg = 1
MIN = 0
MAX = 1


# Variables

X = {(o,m): model.addVar() for o in O for m in M} # can populate like this, not bad - note: indexed via tuple
Y = {(o,m): model.addVar() for o in O for m in M}
S = {(o,m): model.addVar(ub = MaxStorage) for o in O for m in M} # can set bounds on variables too (constraints embedded within variables)


# Objective

model.setObjective(quicksum(SellPrice*X[o,m] - BuyPrice[o][m]*Y[o,m] - StorageCost*S[o,m] for o in O for m in M),GRB.MAXIMIZE) # compare to solution

# Constraints - have not easily referenced them so the dual variables can be called... this requires some knowledge of structure
for m in M:
	model.addConstr(quicksum(X[o,m] for o in O if IsVeg[o]) <= ProductionLimits[Veg])
	model.addConstr(quicksum(X[o,m] for o in O if not IsVeg[o]) <= ProductionLimits[NonVeg])
	model.addConstr(quicksum(X[o,m]*(Hardness[o] - HardnessLimits[MIN]) for o in O) >= 0)
	model.addConstr(quicksum(X[o,m]*(Hardness[o] - HardnessLimits[MAX]) for o in O) <= 0)

	# constrain storage update logically
	if m > 0:
		for o in O:
			model.addConstr(S[o,m] == S[o,m-1] + Y[o,m] - X[o,m])

	# constrain storage contingency - this assumption may be incorrect - discuss with client
for o in O:
	model.addConstr(S[o,0] == StartingLevel + Y[o,0] - X[o,0])
	model.addConstr(S[o,M[-1]] >= StartingLevel) # end with at least as much in storage as you started



model.optimize()

# print out the solution
print "Production:"
for o in O:
	print Oils[o], '=', [round(X[o,m].x,2) for m in M]

print "Purchases:"
for o in O:
	print Oils[o], '=', [round(Y[o,m].x,2) for m in M]

print "Storage:"
for o in O:
	print Oils[o], '=', [round(S[o,m].x,2) for m in M]
