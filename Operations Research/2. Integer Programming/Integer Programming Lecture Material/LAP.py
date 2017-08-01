import math
import random
from gurobipy import *
import pylab

def Distance(p1, p2):
  return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

Num = 200
N = range(Num)
Square = 1000
random.seed(Num)
Plant = [(random.randint(0,Square), random.randint(0,Square)) for i in N]
Job = [(random.randint(0,Square), random.randint(0,Square)) for i in N]

D = [[Distance(Plant[i], Job[j]) for j in N] for i in N]

m = Model('Assignment')
X = [[m.addVar() for j in N] for i in N]

m.update()

m.setObjective(quicksum(D[i][j]*X[i][j] for i in N for j in N))

C1 = [m.addConstr(quicksum(X[i][j] for j in N) == 1) for i in N]
C2 = [m.addConstr(quicksum(X[i][j] for i in N) == 1) for j in N]

m.optimize()

[pylab.plot(Plant[i][0], Plant[i][1], color='black', marker='*') for i in N]
[pylab.plot([Plant[i][0], Job[j][0]], [Plant[i][1], Job[j][1]], 'black') 
  for i in N for j in N if X[i][j].x > 0.99]

pylab.show()
