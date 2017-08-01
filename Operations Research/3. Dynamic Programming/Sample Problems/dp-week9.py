# DP8 Altitude Sickness

Arcs8 = {
    'A': { 'D':6, 'B':10, 'C':7 },
    'B': { 'E':9 },
    'C': { 'E':7 },
    'D': { 'E':11, 'F':7 },
    'E': { 'G':8, 'H':7, 'I':10 },
    'F': { 'G':8, 'H':6, 'I':7 },
    'G': { 'J':13 },
    'H': { 'J':8 },
    'I': { 'J':9 }
}

def dp8(n):
    if n == 'J':
        return (0,'You made it!')
    else:
        return min( (max(Arcs8[n][j], dp8(j)[0]), j)  for j in Arcs8[n])

# DP14 Shortest Path

Arcs14 = {
    'A': { 'B':15, 'C':12 },
    'B': { 'D':9, 'G':10, 'E':7 },
    'C': { 'E':8, 'H':16, 'F':9 },
    'D': { 'G':13, 'J':14 },
    'E': { 'G':11, 'H':5, 'I':12 },
    'F': { 'I':6 },
    'G': { 'K':11, 'J':6 },
    'H': { 'J':9 },
    'I': { 'J':10, 'L':12 },
    'J': { 'K':8, 'Z':12, 'L':9 },
    'K': { 'Z':11 },
    'L': { 'Z':13 }
}

# We use Counter to count how many times dp14() is called before and after adding the memoisation
Counter = 0
_dp14 = {}
def dp14(n):
    global Counter
    Counter += 1
    if n == 'Z':
       return (0,'You made it!')
    else:
        _dp14[n] = min( (Arcs14[n][j] + dp14(j)[0], j)  for j in Arcs14[n])
    return _dp14[n]

# Work through values to display the optimal path
def Answer14():
    n = 'A'
    while n != 'You made it!':
        nextn = dp14(n)
        print(nextn)
        n = nextn[1]

# DP13 Chess Strategy
def dp13(game,points):
    if game == 3:
        if points > 1:
            return (1, 'Win')
        elif points < 1:
            return (0, 'Lost')
        else:
            return (0.45, 'Bold')
    else:
        bold = 0.45*dp13(game+1,points+1)[0] + 0.55*dp13(game+1,points+0)[0]
        conservative = 0.9*dp13(game+1,points+0.5)[0] + 0.1*dp13(game+1,points+0)[0]
        return max([(bold,'Bold'), (conservative,'Conservative')])

# DP5 Another Nonlinear Objective
Usage = {1:3, 2:2, 3:1}
Offset = {1:5, 2:1, 3:2}       
def dp5(t,s):
    if t == 3:
        x = int(s/Usage[t])
        return (x+Offset[t], x, s-x*Usage[t] )
    else:
        return max( ((x + Offset[t])*dp5(t+1,s-x*Usage[t])[0], x, s-x*Usage[t]) 
            for x in range(int(s/Usage[t])+1))

# dp5() above matches what we did on paper by defining stage 3 as the final stage
# In practice that stage is the same as all the others so it is easier to added a dummy stage 4
def dp5a(t,s):
    if t == 4:
        return (1,'Done')
    else:
        return max( ((x + Offset[t])*dp5a(t+1,s-x*Usage[t])[0], x, s-x*Usage[t]) 
            for x in range(int(s/Usage[t])+1))
    
    
    
    
    