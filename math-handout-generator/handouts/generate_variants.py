import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('/Users/yangyake/IdeaProjects/math/handouts/images', exist_ok=True)

def draw_shape(filename, points, edges, labels_offset, azim=-60, elev=20):
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')
    for start, end, style in edges:
        p1, p2 = points[start], points[end]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], style, color='k', linewidth=1.5)

    for name, pt in points.items():
        offset = labels_offset.get(name, (0.1, 0.1, 0.1))
        ax.text(pt[0]+offset[0], pt[1]+offset[1], pt[2]+offset[2], name, fontsize=12)
        ax.plot([pt[0]], [pt[1]], [pt[2]], 'ko', markersize=3)

    ax.set_axis_off()
    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()
    plt.savefig(f'/Users/yangyake/IdeaProjects/math/handouts/images/{filename}', dpi=300)
    plt.close()

# V1: P-ABCD square base
pts1 = {'A': [0,0,0], 'B': [2,0,0], 'C': [2,2,0], 'D': [0,2,0], 'P': [0,1,1.732], 'E': [1,0.5,0.866]}
edges1 = [('A','B','-'),('B','C','-'),('C','D','-'),('D','A','--'),('P','A','-'),('P','B','-'),('P','C','-'),('P','D','-'),('A','E','--'),('C','E','--')]
offsets1 = {'A':(-0.2,-0.2,0), 'B':(0.1,-0.1,0), 'C':(0.1,0.1,0), 'D':(-0.2,0.1,0), 'P':(0,0,0.1), 'E':(0.1,0,0.1)}
draw_shape('var1.png', pts1, edges1, offsets1, azim=-60)

# V2: P-ABC PA perp base, AB perp BC
pts2 = {'A': [0,0,0], 'B': [2,0,0], 'C': [2,2,0], 'P': [0,0,2], 'M': [1,0,1]}
edges2 = [('A','B','--'),('B','C','-'),('A','C','--'),('P','A','-'),('P','B','-'),('P','C','-')]
offsets2 = {'A':(-0.2,-0.2,0), 'B':(0.1,-0.1,0), 'C':(0.1,0.1,0), 'P':(0,0,0.1), 'M':(0.1,0,0.1)}
draw_shape('var2.png', pts2, edges2, offsets2, azim=-45)

# V3: ABCDEF
pts3 = {'A': [0,0,0], 'D': [0,2,0], 'C': [2,2,0], 'B': [4,0,0], 'E': [0,2,2], 'F': [0,0,2]}
edges3 = [('A','B','-'),('B','C','-'),('C','D','-'),('A','D','--'),('F','A','-'),('E','D','--'),('F','E','-'),('F','B','-'),('E','C','-')]
offsets3 = {'A':(-0.2,-0.2,0), 'B':(0.1,-0.1,0), 'C':(0.1,0.1,0), 'D':(-0.2,0.1,0), 'E':(0,0,0.1), 'F':(0,0,0.1)}
draw_shape('var3.png', pts3, edges3, offsets3, azim=-60)

# V4: P-ABCD rect, PA perp
pts4 = {'A':[0,0,0], 'B':[4,0,0], 'C':[4,2,0], 'D':[0,2,0], 'P':[0,0,2], 'E':[2,2,0], 'F':[3,0,0.5]}
edges4 = [('A','B','-'),('B','C','-'),('C','D','-'),('A','D','--'),('P','A','-'),('P','B','-'),('P','C','-'),('P','D','-'),('E','F','--'),('A','E','--'),('A','F','-')]
offsets4 = {'A':(-0.2,-0.2,0), 'B':(0.1,-0.1,0), 'C':(0.1,0.1,0), 'D':(-0.2,0.1,0), 'P':(0,0,0.1), 'E':(0.1,0.1,0), 'F':(0.1,0,0.1)}
draw_shape('var4.png', pts4, edges4, offsets4, azim=-60)

# V5: P-ABCD right trap, PAD eq tri
pts5 = {'A':[0,-1,0], 'D':[0,1,0], 'B':[1,-1,0], 'C':[1,0,0], 'P':[0,0,1.732], 'E':[0,0.5,0.866]}
edges5 = [('A','B','-'),('B','C','-'),('C','D','-'),('A','D','--'),('P','A','-'),('P','B','-'),('P','C','-'),('P','D','-'),('C','E','--'),('P','E','-')]
offsets5 = {'A':(-0.2,-0.2,0), 'B':(0.1,-0.1,0), 'C':(0.1,0.1,0), 'D':(-0.2,0.1,0), 'P':(0,0,0.1), 'E':(0.1,0,0.1)}
draw_shape('var5.png', pts5, edges5, offsets5, azim=-60)

