from __future__ import print_function
import numpy as np
from markovChain import markovChain
from usefulFunctions import partition

class randomWalk(markovChain):
    #A random walk where we move up and down with rate 1.0 in each state between bounds m and M.
    #For the transition function to work well, we define some class variables in the __init__ function.
    def __init__(self,m,M,direct=False):
        super(randomWalk, self).__init__(direct=direct) #always use this as first line when creating your own __init__ 
        self.initialState = m
        self.m = m
        self.M = M
        self.uprate = 1.0
        self.downrate = 1.0   
        
    def transition(self,state):
        #Using a dictionary here is quite simple! 
        rates = {}
        if self.m < state < self.M:
            rates[state+1] = self.uprate 
            rates[state-1] = self.downrate 
        elif state == self.m:
            rates[state+1] = self.uprate 
        elif state == self.M:
            rates[state-1] = self.downrate 
        return rates
            
class randomWalkMulti(markovChain):
    #Now we move up an down on multiple dimensions. 
    def __init__(self,m,M,n,direct=False):
        super(randomWalkMulti, self).__init__(direct=direct)
        assert n > 1 and isinstance(n,int), "n should be an integer greater than 1"
        self.initialState = tuple([m]*n)
        self.n = n
        self.m = m
        self.M = M
        self.uprate = 1.0
        self.downrate = 1.0 
        
    def tupleAdd(self,state,i,b):
        #add amount 'b' to entry 'i' of tuple 'state'.
        newstate = list(state)
        newstate[i] += b
        return tuple(newstate)

    def transition(self,state):
        #now we need to loop over the states
        rates = {}
        for i in range(n):
            if self.m < state[i] < self.M:
                rates[self.tupleAdd(state,i,1)] = self.uprate 
                rates[self.tupleAdd(state,i,-1)] = self.downrate 
            elif state[i] == self.m:
                rates[self.tupleAdd(state,i,1)] = self.uprate 
            elif state[i] == self.M:
                rates[self.tupleAdd(state,i,-1)] = self.downrate 
        return rates               

class randomWalkNumpy(markovChain):
    #Now we do the same thing with a transition function that returns a 2d numpy array.
    #We also specify the statespace function so we can use the direct method.
    #This one is defined immediately for general n.
    def __init__(self,m,M,n,direct=True):
        super(randomWalkNumpy, self).__init__(direct=direct)
        self.initialState = m*np.ones(n,dtype=int)
        self.n = n
        self.m = m
        self.M = M
        self.uprate = 1.0
        self.downrate = 1.0        

        #It is useful to define the variable 'events' for the the transition function.
        #The possible events are 'move up' or 'move down' in one of the random walks.
        #The rates of these events are given in 'eventRates'.
        self.events = np.vstack((np.eye(n,dtype=int),-np.eye(n,dtype=int)))
        self.eventRates = np.array([self.uprate]*n+[self.downrate]*n)  

    def transition(self,state):
        #First check for the current state which of the 'move up' and 'move down' events are possible. 
        up = state < self.M 
        down = state > self.m
        possibleEvents = np.concatenate((up,down)) #Combine into one boolean array. 

        #The possible states after the transition follow by adding the possible 'move up'/'move down' events to the current state.
        newstates = state+self.events[possibleEvents]
        rates = self.eventRates[possibleEvents]
        return newstates,rates   
        
    def statespace(self):
        #Each random walk can be in a state between m and M.
        #The function partition() gives all partitions of integers between min_range and max_range.
        min_range = [self.m]*self.n
        max_range = [self.M]*self.n
        return partition(min_range,max_range) 
        
if __name__ == '__main__': 
    import time    

    P = np.array([[0.5,0.5],[0.6,0.4]])
    mc = markovChain(P)
    mc.computePi('linear')
    print(mc.pi)
    
    #for a one-dimensional state space, calculate the steady state distribution.
    #provided uprate and downrate are the same, each state is equally likely        
    m = 0; M = 5    
    mc = randomWalk(m,M)
    mc.computePi('linear')
    mc.printPi()    
    
    mc = randomWalkNumpy(m,M,n=1)
    mc.computePi('linear')
    mc.printPi()  
    
    mc = randomWalkNumpy(0,2,n=2)
    mc.computePi('linear')
    mc.printPi()
    
    #When states are scalar integers, the indirect method is faster here. 
    #The linear algebra solver is quite fast for these one-dimensional problems (here, krylov and power method have really poor performance)
    M = 100000
    tm=time.clock(); randomWalk(m,M).computePi('linear'); print("Indirect:",time.clock()-tm)
    tm=time.clock(); randomWalkNumpy(m,M,n=1).computePi('linear'); print("Direct:", time.clock()-tm)       
         
    
    #Now a multidimensional case with an equal number of states.
    #Since building the state space is much more complex, the direct approach is faster. 
    #Here the krylov method and power method seem to work best. 
    #The linear algebra solver has memory problems, likely due to fill up of the sparse matrix.
    n = 5; m = 0; M = 9
    tm=time.clock(); randomWalkMulti(m,M,n).computePi('krylov'); print("Indirect:", time.clock()-tm)
    tm=time.clock(); randomWalkNumpy(m,M,n).computePi('krylov'); print("Direct:",time.clock()-tm)


