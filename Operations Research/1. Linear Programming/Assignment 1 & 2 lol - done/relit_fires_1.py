from gurobipy import *

"""
First assignment.

Fertiliser company wanting to improve on importing their raw material (diammonium phosphate).
Ship into ports of Brisbane, Sydney, and Melbourne. Each feed into local factories.
Predictions have been laid out for the demands (tonnes) and costs ($/tonne) for the next 8 quarters.

Each quarter a single ship is used for imports with a capacity of 5000 tonnes.
Currently have 1500 tonnes in Brisbane, 2100 tonnes in Sydney, and 1800 tonnes in Melbourne.
Can store any material on hand at the end of the quarter for a cost of $1.50 per tonne.

i)
Minimise cost over the next 8 quarters while satisfying demand.

First 'guess' $1883865 - was subtracting storage costs...
Second 'guess' $1956415 - correct

ii)
Want to retain same amounts in storage at the end of the 8 quarters as they started with.
Solution $1666525 - idiot - how the hell did your costs reduce with an additional constraint - this is the first check!
Actual Solution $2468400 - you can't remove the restriction relating the final storage to the previous

iii)
Introduce maximum storages: [3200, 4300,1800]
Solution $2468750 - very slight increase

iv)
Pay $20,000 to use the ship in each quarter.
Pay $8,000 each time the ship visits one of ports in each quarter
Let's see if we can optimise by reducing ship usage.

Solution:
$2720025 - had to use binary variables? then what was he on about?

v)
Can use a bigger ship 8 tonne capacity for $28,000 per quarter (same per port cost).
Can only use one ship per quarter though.

Solution:
$2441425

vi)
Now they also want to import urea. Still only using one ship though.
Max storage facilities are duplicated

Solution:
$3288552.5

vii)
Ship has various holds - need to be used as materials cannot mix in transit.
Smaller ship has 5x1000 tonne holds. Larger ship has 8x1000 tonne holds.

Solution:
$3199049 - wrong - hold doesn't match imported - needed to restrict urea holds and total urea as well as DP individually (ofc)
$3311070

lol - presolve removed 410 rows and 130 columns - lots of redundancy in my formulation...

viii)
Not always using the larger ship so the company requests we don't use it for two quarters in a row.
Test the cost impact of this restriction.

Solution:
$3386187.5

"""

# Sets/Data

Quarter = { # structure is Quarter : (Cost, Brisbane Demand, Sydney Demand, Melbourne Demand)
		1 : ( 840, 1550, 1410, 87, 525, 390,  845, 44),
		2 : (1290, 1420, 1050, 63, 540, 555,  865, 70),
		3 : (1380,  950, 1290, 85, 515,	460,  590, 72),
		4 : ( 730, 2130, 1940, 94, 630,	720,  780, 49),
		5 : ( 790, 1360, 1610, 60, 565, 425,  955, 72),
		6 : (1220, 1310, 2000, 67, 550,	415,  660, 47),
		7 : (1360, 1040, 1650, 91, 585,	665, 1020, 49),
		8 : (1500, 1670, 1560, 63, 565,	780,  920, 75)
		}

Products = ["DP","Urea"]
ProductsCost = [3,7] # index for quarters

P = range(len(Products))

U = range(4,7)



ImportLimit1 = 5000 # tonnes/quarter
ImportLimit2 = 8000
StorageCost = 1.5 # $/tonne
InitialDPStorage = [1500, 2100, 1800]
InitialUStorage = [None, None, None, None, 700, 600, 900] # so dodgy
MaxStorage = [3200, 4300, 1800, None, 3200, 4300, 1800] # bit hacky with indexing - should work
ShipCost1 = 20000
ShipCost2 = 28000
CostPerPort = 8000

HoldSize = 1000

City = ["Brisbane", "Sydney", "Melbourne"]
C = range(len(City))

# Variables

model = Model("Importing")

# import variables
X = {(q,c): model.addVar() for q in Quarter for c in C}

# storage variables
S = {(q,c): model.addVar() for q in Quarter for c in C}

# add urea variables
for q in Quarter:
	for u in U:
		X.update({(q,u): model.addVar()})
		S.update({(q,u): model.addVar()})

# ship usage binary variables
ShipPortUsage = {(q,c): model.addVar(vtype = GRB.BINARY) for q in Quarter for c in C}
ShipUsage1 = {q: model.addVar(vtype = GRB.BINARY) for q in Quarter}
ShipUsage2 = {q: model.addVar(vtype = GRB.BINARY) for q in Quarter}
#ShipUsage = [model.addVar() for q in Quarter] # results in indexing issues

Ships = [5,8]

Sh = range(len(Ships))

# Hold Usage binary variables and quantity variables

H = {(q,s,h,p): model.addVar() for q in Quarter for s in Sh for h in range(Ships[s]) for p in P}
Y = {(q,s,h,p): model.addVar(vtype = GRB.BINARY) for q in Quarter for s in Sh for h in range(Ships[s]) for p in P}

# Objective

model.setObjective(quicksum(X[q,c]*Quarter[q][ProductsCost[0]] + S[q,c]*StorageCost for q in Quarter for c in C) +
				   quicksum(X[q,u]*Quarter[q][ProductsCost[1]] + S[q,u]*StorageCost for q in Quarter for u in U) + 
				   quicksum(ShipPortUsage[q,c]*CostPerPort for q in Quarter for c in C) +
				   quicksum(ShipUsage1[q] * ShipCost1 + ShipUsage2[q] * ShipCost2 for q in Quarter)
				   , GRB.MINIMIZE)

# Constraints

M = 8000 # import limit restricts the value

for q in Quarter:
	# adjust import limits based on which ship is used
	model.addConstr(quicksum(X[q,c] for c in C) + quicksum(X[q,u] for u in U) <= ImportLimit1*ShipUsage1[q] + ImportLimit2*ShipUsage2[q])

	# ensure at most one ship is used
	model.addConstr(ShipUsage1[q] + ShipUsage2[q] <= 1)

	# DP storage constraints
	for c in C:
		model.addConstr(S[q,c] <= MaxStorage[c])
	# Urea storage contraints
	for u in U:
		model.addConstr(S[q,u] <= MaxStorage[u])

	if q == 1:
		for c in C:
			model.addConstr(S[q,c] == InitialDPStorage[c] + X[q,c] - Quarter[q][c])
		for u in U:
			model.addConstr(S[q,u] == InitialUStorage[u] + X[q,u] - Quarter[q][u])
	else:
		for c in C:
			model.addConstr(S[q,c] == S[q-1,c] + X[q,c] - Quarter[q][c])
		for u in U:
			model.addConstr(S[q,u] == S[q-1,u] + X[q,u] - Quarter[q][u])
	
	if q == 8:
		for c in C:
			model.addConstr(S[q,c] == InitialDPStorage[c]) # final storage is the same
		for u in U:
			model.addConstr(S[q,u] == InitialUStorage[u])

	# Big M constraints for binary/indicator variables
	for c in C:
		u = c + 4
		model.addConstr(ShipPortUsage[q,c]*M >= X[q,c] + X[q,u])

	# constraint for general usage binary variable
	# model.addConstr(quicksum(ShipPortUsage[q,c] for c in C) <= 3*ShipUsage[q])
	# equivalently - deprecated
	model.addConstr(quicksum(X[q,c] for c in C) + quicksum(X[q,u] for u in U) <= M*(ShipUsage1[q] + ShipUsage2[q]))

	# hold constraints
		# import quantities are the same as hold quantities
	# model.addConstr(quicksum(X[q,c] for c in C) + quicksum(X[q,u] for u in U) == quicksum(H[q,s,h,p] for s in Sh for h in range(Ships[s]) for p in P))
	model.addConstr(quicksum(X[q,c] for c in C) == quicksum(H[q,s,h,0] for s in Sh for h in range(Ships[s])))
	model.addConstr(quicksum(X[q,u] for u in U) == quicksum(H[q,s,h,1] for s in Sh for h in range(Ships[s])))

		# limit holds to 1000 AND ensure they only hold one or the other AND indicate which it is

	# indicate a ship is being used
	model.addConstr(5*ShipUsage1[q] >= quicksum(Y[q,0,h,p] for h in range(Ships[0]) for p in P))
	model.addConstr(8*ShipUsage2[q] >= quicksum(Y[q,1,h,p] for h in range(Ships[1]) for p in P))

	for s in Sh:
		for h in range(Ships[s]):
			# can only hold one or the other
			model.addConstr(quicksum(Y[q,s,h,p] for p in P) <= 1)

			for p in P:
				# limit holds to 1000
				model.addConstr(H[q,s,h,p] <= HoldSize)		

				# indicator variables
				model.addConstr(HoldSize*Y[q,s,h,p] >= H[q,s,h,p])

	# final constraint - can't use ship 2 for two consecutive quarters
	if q > 1:
		model.addConstr(ShipUsage2[q] + ShipUsage2[q-1] <= 1)

# Solution

model.optimize()

print "\nImports:"
for q in Quarter:
	print "Quarter:", q, "DP Imported:", [X[q,c].x for c in C]
	print "Quarter:", q, "Urea Imported:", [X[q,u].x for u in U]

print "\nStorage:"
for q in Quarter:
	print "Quarter:", q, "DP Stored:", [S[q,c].x for c in C] 
	print "Quarter:", q, "Urea Stored:", [S[q,u].x for u in U] 


print "\nShip Usage"
for q in Quarter:
	print "Quarter:", q, "Ship Usage:", [ShipPortUsage[q,c].x for c in C]

for q in Quarter:
	print "Quarter:", q, "Ship 1 & 2 Usage:", [ShipUsage1[q].x, ShipUsage2[q].x]

print "\nShip Hold Usage"
for q in Quarter:
	for s in Sh:
		for p in P:
			print "Quarter:", q, "Ship", s, "Product", Products[p], "Hold Urea Usage:", [H[q,s,h,p].x for h in range(Ships[s])]

print "\nShip Hold Usage Binary"
for q in Quarter:
	for s in Sh:
		for p in P:
			print "Quarter:", q, "Ship", s, "Product", Products[p], "Hold Urea Usage:", [Y[q,s,h,p].x for h in range(Ships[s])]