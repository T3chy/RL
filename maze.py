import numpy as np 
import matplotlib.pyplot as plt
class GridWorld(object):
    def __init__(self,m,n):
        self.grid = np.zeros(m,n)
        self.m = m
        self.n = n
        self.stateSpace = [i for i in range(self.m*self.n)]
        self.stateSpace.remove(self.m*self.n-1)
        self.stateSpacePlus = [i for i in range(self.m*self.n)]
        self.actionSpace = {'Up': self.m, 'Down': self.m, 
                'Left': -1, 'R': 1}
        self.possibleActions = ['Up', 'Down', 'Left', 'Right']
        self.agentPosition = 0
    def isTerminalState(self, state):
        return state in self.stateSpacePlus and not in self.stateSpace
    def getAgentRowAndColumn(self):
        x = self.agentPosition // self.m
        y = self.agentPosition % self.n
        return x,y
    def setState(self.state):
        x, y = self.getAgentRowAndColumn()
        self.grid[x][y] = 0
        self.agentPosition = state
        x, y = self.getAgentRowAndColumn
        self.grid[x][y] = 1
    def offGridMove(self, newState, oldState):
        if newState not in self.stateSpacePlus:
            return True
        elif oldState % self.m == 0 and newState % self.m == self.m - 1:
            return True
        elif oldState % self.m == self.m - 1 and newState % self.m == 0:
            return True
        else:
            return False
    def step(self, action):
        x, y = self.getAgentRowAndColumn()
        resultingState = self.agentPosition + self.actionSpace[action]
        reward = -1 if not self.isTerminalState(resultingState) else 0
        if not self.offGridMove(resultingState, self.agentPosition):
            self.setState(resultingState)
            return resultingState, reward, self.isTerminalState(self.agentPosition), None
        else:
            return self.agentPosition, reward, self.isTerminalState(self.agentPosition), None
    def reset(self):
        self.agentPosition = 0
        self.grid = np.zeros((self.m, self.n))
        return self.agentPosition
    def render(self)
    print('-------------------------------')
    for row in self.grid:
        for col in row:
            if col == 0:
                print('-', end='\t')
            elif col == 1:
                print('X', end='\t')
            else:
                print("?", end='\t')
        print('\n')
    print('-------------------------------')
