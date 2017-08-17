from gurobipy import *

"""
Refinement of raw oils and blending optimally (per tonne).
2 types of vege oils are made and 3 types of non-vege oils.


Solution: - it's always important to sanity check for debugging purposes
Make $15,259.26 by producing 125.93 tonnes of Veg 1, 74.07 tonnes of Veg 2, and 200 tonnes of Oil 2.

And I'm wrong... - I had Veg ProductionLimits for NonVeg as well... easy to check via the 200 tonnes restriction
Correct is make $17,592.59 by producing 159.26 tonnes of Veg 1, 40.74 tonnes of Veg 2, and 250 tonnes of Oil 2.

"""

m = Model()

# Sets

Oils = ["Veg 1", "Veg 2", "Oil 1", "Oil 2", "Oil 3"]

# Data

Cost = [110,120,130,110,115] # $/tonne
Hardness = [8.8,6.1,2.0,4.2,5.0] # some unit
ProductionLimits = [200,250] # tonnes of vege oil and non-vege oil respectively
HardnessLimits = [3,6] # lower and upper bounds
SellPrice = 150 # $/tonne

O = range(len(Oils))
OVeg = range(len(Oils)-3)
ONonVeg = range(len(Oils)-3,len(Oils))
Veg = 0
NonVeg = 1
MIN = 0
MAX = 1


# Variables

X = {}
for o in O:
	X[o] = m.addVar()

# Objective

m.setObjective(quicksum((SellPrice - Cost[o])*X[o] for o in O),GRB.MAXIMIZE)

# Constraints
Y = {}
for i in range(4):
	Y [i] = m.addConstr(quicksum(X[o] for o in OVeg) <= ProductionLimits[Veg])
	Y [i] = m.addConstr(quicksum(X[o] for o in ONonVeg) <= ProductionLimits[NonVeg])
	Y [i] = m.addConstr(quicksum(X[o]*(Hardness[o] - HardnessLimits[MIN]) for o in O) >= 0)
	Y [i] = m.addConstr(quicksum(X[o]*(Hardness[o] - HardnessLimits[MAX]) for o in O) <= 0)

m.optimize()

# print out the solution
for o in O:
	print Oils[o], '=', X[o].x


