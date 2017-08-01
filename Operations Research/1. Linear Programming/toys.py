from gurobipy import *

m = Model()

x1 = m.addVar()
x2 = m.addVar()

m.setObjective(3*x1+2*x2, GRB.MAXIMIZE)

c1 = m.addConstr(2*x1+x2<=100)
c2 = m.addConstr(x1+x2<=80)
c3 = m.addConstr(x1<=40)

m.optimize()

print(x1.SAObjLow, x1.obj, x1.SAObjUp)
print(x2.SAObjLow, x2.obj, x2.SAObjUp)

print(c1.pi, c1.Slack, c1.SARHSLow, c1.RHS, c1.SARHSUp)
print(c2.pi, c2.Slack, c2.SARHSLow, c2.RHS, c2.SARHSUp)
print(c3.pi, c3.Slack, c3.SARHSLow, c3.RHS, c3.SARHSUp)