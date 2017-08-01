import pylab

starvation = 25
egglaying = 80

webs = range(3)
size = [4, 8, 12]
prey = [0.66, 0.77, 0.82]
predator = [0.01, 0.02, 0.03]

basel = 0.4
N = 6

days = 10

# calculate the energy cost for a weight and web size
def expend(weight,w):
    return -0.125*size[w] + 0.005*weight*size[w]

# for a fractional weight, discretize() combines the future values of the two
# neighbouring integer states
def discretize(day,weight):
    x = int(weight)
    p = weight - x
    return p*orb(day,x+1)[0] + (1-p)*orb(day,x)[0]

orbs = {}
def orb(day,weight):
    
    if not (day,weight) in orbs:
        
        if weight >= egglaying:
            orbs[day,weight] = (1, 'eggs')
            
        elif weight < starvation:
            orbs[day,weight] = (0, 'died')
        
        elif day >= days:
            orbs[day,weight] = (0, 'outoftime')
       
        else:
            orbs[day,weight] = max([(predator[w]*0 +
                (1-predator[w])*prey[w]*discretize(day+1,weight-basel-expend(weight,w)+N) +
                (1-predator[w])*(1-prey[w])*discretize(day+1,weight-basel-expend(weight,w)),size[w])
                 for w in webs])
    return orbs[day,weight]

# plot best web size for varying weights at start of day 0
xs = [j for j in range(30,79)]
ys = [orb(0,x)[1] for x in xs]
pylab.plot(xs,ys)
pylab.ylim([0,13])
pylab.xlim([25,80])
pylab.xlabel('Weight (mg) on Day 1')
pylab.ylabel('Optimal web size (m) for Day 1')
pylab.show()