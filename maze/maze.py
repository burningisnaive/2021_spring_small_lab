import numpy as np
import matplotlib.pyplot as plt
import tools 


clist = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def updateQ(q1, a1, q2, a2):
    if q1 is None:
        return q2, a2
    if q1 > q2:
        return q1, a1
    else:
        return q2, a2    

class maze():
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.maze_array = np.zeros([h,w], dtype=np.uint8)

    def flip_block(self, x, y):
        idx_h = y
        idx_w = x
        if idx_h<0 or idx_h>=self.h or idx_w<0 or idx_w>=self.w:
            print('invalid position (%d, %d)' %(idx_h, idx_w))
            return 

        self.maze_array[idx_h, idx_w] = 1- self.maze_array[idx_h, idx_w]

    def set_array(self, map):    
        if len(map.shape) > 2:
            print('invalid array of shape', map.shape)
            return

        if map.shape[0] != self.h or map.shape[1] != self.w:
            print('invalid array of shape', map.shape)
            return

        self.maze_array = np.array(map>0.5, dtype=np.uint8)  

    def show_maze(self, ax: plt.Axes):    
        ax.plot([0, 0], [0, self.h], color=clist[0])
        ax.plot([self.w, self.w], [0, self.h], color=clist[0])
        ax.plot([0, self.w], [0, 0], color=clist[0])
        ax.plot([0, self.w], [self.h, self.h], color=clist[0])

        for i in range(self.h):
            for j in range(self.w):
                if self.maze_array[i,j]:
                    tools.plot_block(ax, j, i, clist[0])

    def next_state(self, x, y):
        ret = []
        if self.maze_array[y, x] == 1:
            return ret

        xlist = [x-1, x, x, x+1, x]
        ylist = [y, y-1, y+1, y, y]     
        for i in range(4):
            tmpx = xlist[i]
            tmpy = ylist[i]
            if tmpx>=0 and tmpx<self.w and tmpy>=0 and tmpy<self.h:
                if self.maze_array[tmpy,tmpx] == 0:
                    ret.append((tmpx, tmpy))
        return ret        
     
    def is_empty(self, tmpx, tmpy):
        if tmpx>=0 and tmpx<=self.w and tmpy>=0 and tmpy<self.h:
            if self.maze_array[tmpy,tmpx] == 0:
                return True
        return False        

class Q_learning_maze():
    def __init__(self, MAZE: maze, desti):
        self.MAZE = MAZE
        self.desti = desti
        self.gamma = 0.9
        self.Q_s_a = {}     
        self.V_s = {}
        self.policy = {}
        
        for x in range(self.MAZE.w):
            for y in range(self.MAZE.h):
                state = (x, y)
                actions = self.MAZE.next_state(x, y)
                if len(actions) < 1:
                    continue
                self.Q_s_a[state] = {}      # Q 
                self.V_s[state] = 0         # V
                self.policy[state] = None    
                for a in actions:
                    self.Q_s_a[state][a] = 0

    def reward_score(self, state, action):
        # if we arrive, reward is 0 otherwise -1
        if self.state_transform(state, action) == self.desti:
            return 0
        else:
            return -1    

    def state_transform(self, state, action):
        return action # next state is just the action       

    def value_iteration(self, loop=10, ax=None):
        for idx in range(loop):
            Q_loop = []
            for s in self.V_s:
                best_act = None
                best_Q = None
                for a in self.Q_s_a[s]:
                    next_s = self.state_transform(s, a)
                    self.Q_s_a[s][a] = (self.gamma*self.V_s[next_s] + self.reward_score(s, a))
                    best_Q, best_act = updateQ(best_Q, best_act, self.Q_s_a[s][a], a)
                    Q_loop.append(np.absolute(best_Q))
                self.policy[s] = best_act

            for s in self.V_s:
                self.V_s[s] = self.Q_s_a[s][self.policy[s]]    

            plt.cla()
            self.MAZE.show_maze(ax)
            for s in self.V_s:
                tools.show_state_q(ax, s, self.Q_s_a[s])
        
            plt.show()
            plt.pause(0.05)



if __name__ =='__main__':
    plt.ion()
    MAZE = maze(10, 15)
    MAZE.set_array(np.random.rand(10, 15)>0.7)

    ax = plt.subplot(1,1,1)
    MAZE.show_maze(ax)
    plt.show()

    modify_map = (input('continue modification?(y/n):') == 'y')
    while(modify_map):
        tmp = input('block(int int):')
        tmp.strip()
        block = (int(v) for v in tmp.split()) 
        MAZE.flip_block(*block)
        plt.cla()
        MAZE.show_maze(ax)
        plt.show()
        modify_map = (input('continue modification?(y/n):') == 'y')

    start = (-1, -1)
    desti = (-1, -1)
    while(not MAZE.is_empty(*start)):
        tmp = input('start position(int int):')
        tmp.strip()
        start = tuple(int(v) for v in tmp.split())

    while(not MAZE.is_empty(*desti)):
        tmp = input('destination position(int int):')
        tmp.strip()
        desti = tuple(int(v) for v in tmp.split())       

    solver = Q_learning_maze(MAZE=MAZE, desti=desti)
    solver.value_iteration(loop=30, ax=ax)    

    tools.plot_block(ax, start[0], start[1], clist[1])
    tools.plot_block(ax, desti[0], desti[1], clist[2])
    plt.show()    

    state = start
    while state != desti:
        old_s = (state[0], state[1])
        state = solver.policy[state]
        #print(state)
        tools.show_move(ax, old_s, state)

    plt.ioff()

    a = input('input anything to quit')


