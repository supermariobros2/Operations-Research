from gurobipy import *

"""
Basic network model implementation. Could be quite useful for modelling work in future (e.g. stock pile reclaimation)

Solution:
Optimal Objective: 510
- all constraints met
- non-unique / well underconstrained

"""

# Sets

N = { # if only one descriptor then index as N[n], else N[n][0]
	1:  (50),
	2:  (95),
	3:  (35),
	4:  (75),
	5:  (0),
	6:  (0),
	7:  (0),
	8:  (0),
	9:  (-80),
	10: (-40),
	11: (-70),
	12: (-65),
}

# check it's zero-sum
total = 0
for n in N:
	total += N[n]

if total != 0: print "This formulation is incorrect."

# generate arcs based on N
A = {}
count = 1
for i in range(1,len(N) - 3):
	fn = i
	if i % 4 == 1:
		tn = i + 4
		A.update({count: (fn,tn)})
		count += 1

		tn = i + 5
		A.update({count: (fn,tn)})
		count += 1

	elif i % 4 == 0:
		tn = i + 3
		A.update({count: (fn,tn)})
		count += 1

		tn = i + 4
		A.update({count: (fn,tn)})
		count += 1

	else:
		tn = i + 3
		A.update({count: (fn,tn)})
		count += 1

		tn = i + 4
		A.update({count: (fn,tn)})
		count += 1

		tn = i + 5
		A.update({count: (fn,tn)})
		count += 1

# Variables

model = Model("Network")

X = {a: model.addVar() for a in A}

# Objective

c = 1. # set arc-cost to 1
model.setObjective(quicksum(c*X[a] for a in A), GRB.MINIMIZE)

# Constraints
C = {}
count = 1
for n in N:
	C.update({count: model.addConstr(quicksum(X[a] for a in A if A[a][0] == n) - quicksum(X[a] for a in A if A[a][1] == n) == N[n])})
	count += 1

# Solve

model.optimize()

print "\nSolution:"
for a in A:
	print "Arc", a, "From:", A[a][0], "To:", A[a][1], "Amount:", X[a].x