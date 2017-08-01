import pylab

def SongR(t,i,m):
    # Handle case where i is negative (int(-0.1)==0)
    if i<=0:
        return 0
    x = int(i)
    p = i - x
    return p*Song(t+1,x+1,m)[0] + (1-p)*Song(t+1,x,m)[0]

def SongB(t,i,m):
    return 0.25*SongR(t,i+6.4,m)+0.5*SongR(t,i,m)+0.25*SongR(t,i-6.4,m)

_Song = {}
def Song(t,i,m):
    if i<=0:
        return (0, 'Dead')
    if t==150:
        return (m+1, 'Final')
    if (t,i,m) not in _Song:
        if t>=75:
            _Song[t,i,m] = (SongR(t,i-3.6,m),'Rest')
        else:
            _Song[t,i,m] = max(
                    (0.004*SongB(t,i-(12+0.002*i),1)+
                     0.996*SongB(t,i-(12+0.002*i),m),'Sing'),
                    (0.6*SongB(t,i-(8+0.007*i)+32,m)+
                     0.4*SongB(t,i-(8+0.007*i),m),'Forage'),
                    (SongR(t,i-3.6,m),'ZRest'))
    
    return _Song[t,i,m]    

Threshold = [min(i for i in range(1,1000) if Song(t,i,0)[1]=='Sing') 
                for t in range(75)]

pylab.plot(range(75),Threshold)
pylab.xlabel('Time Period')
pylab.ylabel('Sing food reserve threshold')
pylab.show()



