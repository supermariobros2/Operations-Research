from gurobipy import *

# Set up your own data

# Create the Model object
m = Model("Euing Oil")
# Create all your variables
x11 = m.addVar(name="x11")
x12 = m.addVar(name="x12")
x21 = m.addVar(name="x21")
x22 = m.addVar(name="x22")
y = m.addVar(ub=1500,name="y")
#y1 = m.addVar(ub=500,name="y1")
#y2 = m.addVar(ub=500,name="y2")
#y3 = m.addVar(ub=500,name="y3")
#z1 = m.addVar(vtype=GRB.BINARY,name="z1")
#z2 = m.addVar(vtype=GRB.BINARY,name="z2")

#Set the objective
#m.setObjective(1.2*x11+1.2*x21+1.4*x12+1.4*x22-y1*2.5-y2*2-y3*1.5, GRB.MAXIMIZE)
m.setObjective(1.2*x11+1.2*x21+1.4*x12+1.4*x22, GRB.MAXIMIZE)
m.setPWLObj(y,[0,500,1000,1500],[0,-1250,-2250,-3000])
# Add the constraints
m.addConstr(x11+x12<=500+y)
m.addConstr(x21+x22<=1000)
m.addConstr(x11>=x21)
m.addConstr(x12>=1.5*x22)
#m.addConstr(y==y1+y2+y3)
#m.addConstr(y2<=500*z1)
#m.addConstr(y3<=500*z2)
#m.addConstr(y1>=500*z1)
#m.addConstr(y2>=500*z2)
# Optimize
m.optimize()
# Write out the answer
print ("Objective is:", m.objVal)
for v in m.getVars():
    print (v.VarName, round(v.X,2))
