import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'PingFang SC']
matplotlib.rcParams['axes.unicode_minus'] = False
out_dir = '/Users/yangyake/IdeaProjects/math/handouts/images'
os.makedirs(out_dir, exist_ok=True)

def plot_geom(pts, edges, filename, title, elev=20, azim=-60):
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')
    for p1, p2, style in edges:
        x = [pts[p1][0], pts[p2][0]]
        y = [pts[p1][1], pts[p2][1]]
        z = [pts[p1][2], pts[p2][2]]
        ax.plot(x, y, z, color='#1f77b4', linewidth=1.5, linestyle=style)
    for name, p in pts.items():
        ax.scatter(*p, color='red', s=30)
        ax.text(p[0]+0.05, p[1]+0.05, p[2]+0.05, f'{name}', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, pad=10)
    ax.view_init(elev=elev, azim=azim)
    ax.axis('off')

    # ensure equal aspect ratio roughly
    limits = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])

    plt.savefig(os.path.join(out_dir, filename), dpi=300, bbox_inches='tight')
    plt.close()

# Var 1: 正四棱锥
pts1 = {'A': [1, -1, 0], 'B': [1, 1, 0], 'C': [-1, 1, 0], 'D': [-1, -1, 0], 'P': [0, 0, 2], 'O': [0, 0, 0], 'E': [0.5, -0.5, 1]}
edges1 = [('A','B','-'), ('B','C','-'), ('C','D','--'), ('D','A','--'), ('P','A','-'), ('P','B','-'), ('P','C','-'), ('P','D','--'), ('A','C','--'), ('B','D','--'), ('P','O','--'), ('C','E','--')]
plot_geom(pts1, edges1, 'var1_geo.png', '【变式 1】正四棱锥 P-ABCD')

# Var 2: 三棱柱
pts2 = {'C': [0,0,0], 'A': [0,2,0], 'B': [2,0,0], 'C1': [0,0,2], 'A1': [0,2,2], 'B1': [2,0,2]}
edges2 = [('C','A','--'), ('C','B','--'), ('A','B','-'), ('C1','A1','-'), ('C1','B1','-'), ('A1','B1','-'), ('C','C1','--'), ('A','A1','-'), ('B','B1','-'), ('A1','B','-'), ('A1','C','--')]
plot_geom(pts2, edges2, 'var2_geo.png', '【变式 2】三棱柱 ABC-A1B1C1', elev=15, azim=-75)

# Var 3: 四棱锥
pts3 = {'A': [0,0,0], 'B': [1,0,0], 'C': [1,2,0], 'D': [0,2,0], 'P': [0,0,1], 'E': [0,1,0.5]}
edges3 = [('A','B','-'), ('B','C','-'), ('C','D','--'), ('D','A','--'), ('P','A','--'), ('P','B','-'), ('P','C','-'), ('P','D','--'), ('A','C','--'), ('C','E','--'), ('A','E','--')]
plot_geom(pts3, edges3, 'var3_geo.png', '【变式 3】四棱锥 P-ABCD', elev=25, azim=-60)

# Var 4: 翻折后的三棱锥
pts4 = {'A': [0,0,0], 'C': [0,1,0], 'B': [1,1,0], 'P': [0,0,1]}
edges4 = [('A','B','-'), ('B','C','-'), ('C','A','--'), ('P','A','--'), ('P','B','-'), ('P','C','-')]
plot_geom(pts4, edges4, 'var4_geo.png', '【变式 4】三棱锥 P-ABC', elev=20, azim=-50)

# Var 5: 正三棱锥
pts5 = {'A': [1,0,0], 'B': [-0.5, 0.866, 0], 'C': [-0.5, -0.866, 0], 'P': [0,0,1.732], 'M': [-0.25, 0.433, 0.866]}
edges5 = [('A','B','-'), ('B','C','-'), ('C','A','--'), ('P','A','-'), ('P','B','-'), ('P','C','-'), ('A','M','--'), ('C','M','--')]
plot_geom(pts5, edges5, 'var5_geo.png', '【变式 5】正三棱锥 P-ABC', elev=20, azim=-120)

print("All variant images generated.")

