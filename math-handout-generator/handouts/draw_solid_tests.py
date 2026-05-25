import matplotlib.pyplot as plt
import os

os.makedirs('/Users/yangyake/IdeaProjects/math/handouts/images', exist_ok=True)

def draw_shape(filename, points, edges, labels_offset, azim=-60, elev=20):
    fig = plt.figure(figsize=(5, 4))
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

# Test 1 (P-ABCD rhombus, PA perp)
pts_t1 = {'A':[0,0,0], 'B':[2,0,0], 'C':[3,1.732,0], 'D':[1,1.732,0], 'P':[0,0,2.5], 'E':[1, 0, 1.25]}
edges_t1 = [('A','B','-'),('B','C','-'),('C','D','-'),('D','A','--'),('P','A','-'),('P','B','-'),('P','C','-'),('P','D','--'),('D','E','--')]
off_t1 = {'A':(-0.2,-0.2,0), 'B':(0.1,-0.1,0), 'C':(0.1,0.1,0), 'D':(-0.2,0.1,0), 'P':(0,0,0.1), 'E':(0.1,-0.1,0)}
draw_shape('test1_solid.png', pts_t1, edges_t1, off_t1, azim=-60)

# Test 2 (Prism ABC-A1B1C1, angle B=90)
pts_t2 = {'B':[0,0,0], 'A':[0,2,0], 'C':[2,0,0], 'B1':[0,0,3], 'A1':[0,2,3], 'C1':[2,0,3], 'M':[1,1,3]}
edges_t2 = [('A','B','--'),('B','C','--'),('A','C','-'),('A1','B1','-'),('B1','C1','-'),('A1','C1','-'),('A','A1','-'),('B','B1','--'),('C','C1','-'),('B','M','--')]
off_t2 = {'B':(-0.2,-0.2,0), 'A':(0.1,-0.1,0), 'C':(0.1,0.1,0), 'B1':(-0.2,-0.2,0.1), 'A1':(0.1,-0.1,0.1), 'C1':(0.1,0.1,0.1), 'M':(0,0.1,0.1)}
draw_shape('test2_solid.png', pts_t2, edges_t2, off_t2, azim=-45)

# Test 3 (P-ABCD, PD perp ABCD, square)
pts_t3 = {'D':[0,0,0], 'A':[2,0,0], 'B':[2,2,0], 'C':[0,2,0], 'P':[0,0,3], 'E':[1,0,1.5], 'F':[1,1,1.5], 'Q':[0,1,1.5]}
edges_t3 = [('A','B','-'),('B','C','-'),('C','D','--'),('D','A','--'),('P','A','-'),('P','B','-'),('P','C','-'),('P','D','--'),('E','F','-'),('D','Q','--')]
off_t3 = {'D':(-0.2,-0.2,0), 'A':(0.1,-0.1,0), 'B':(0.1,0.1,0), 'C':(-0.2,0.1,0), 'P':(0,0,0.1), 'E':(0.1,-0.1,0), 'F':(0.1,-0.1,0), 'Q':(-0.2,0,0)}
draw_shape('test3_solid.png', pts_t3, edges_t3, off_t3, azim=-60)

