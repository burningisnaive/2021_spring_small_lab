import matplotlib.pyplot as plt
import numpy as np

clist = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def plot_block(ax: plt.Axes, i, j, c):
    x = [i, i+1]
    y1 = [j, j]
    y2 = [j+1, j+1]
    ax.fill_between(x, y1, y2, color=c)

def show_move(ax, s1, s2):
    ax.plot([s1[0]+0.5, s2[0]+0.5], [s1[1]+0.5, s2[1]+0.5], color=clist[5])

def show_q(ax, s1, s2, q):
    if(s1 == s2):
        return

    x1, y1 = s1
    x2, y2 = s2
    x1 += 0.5
    x2 += 0.5
    y1 += 0.5
    y2 += 0.5

    if x1 == x2:
        ax.plot( [x1-0.1, x1], [(y1+y2)/2, (y1+y2)/2 + (y2-y1)*np.exp(q)], color=clist[7])
        ax.plot( [x1+0.1, x1], [(y1+y2)/2, (y1+y2)/2 + (y2-y1)*np.exp(q)], color=clist[7])

    if y1 == y2:  
        ax.plot( [(x1+x2)/2, (x1+x2)/2 + (x2-x1)*np.exp(q)], [y1+0.1, y1], color=clist[7])
        ax.plot( [(x1+x2)/2, (x1+x2)/2 + (x2-x1)*np.exp(q)], [y1-0.1, y1], color=clist[7])

def show_state_q(ax, s, q_a):
    alist = [a for a in q_a]
    alist.sort(key=lambda a: q_a[a])

    for i in range(len(alist)):
        show_q(ax, s, alist[i], i-len(alist))


