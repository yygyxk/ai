import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'PingFang SC']
matplotlib.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Coordinates
E = np.array([0, 0, 0])
A = np.array([1, 0, 0])
B = np.array([0, 1, 0])
C = np.array([-2, 1, 0])
D = np.array([-3, 0, 0])
P = np.array([0, 0, 2])
F = np.array([0, 0.5, 1])

pts = {'E': E, 'A': A, 'B': B, 'C': C, 'D': D, 'P': P, 'F': F}

# Edges to plot
edges = [
    ('P', 'A'), ('P', 'B'), ('P', 'C'), ('P', 'D'),
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'),
    ('P', 'E'), ('B', 'E'), ('A', 'F')
]

for p1, p2 in edges:
    x = [pts[p1][0], pts[p2][0]]
    y = [pts[p1][1], pts[p2][1]]
    z = [pts[p1][2], pts[p2][2]]
    line_style = '-'
    # dashed lines for hidden edges
    if (p1, p2) in [('C', 'D'), ('D', 'A'), ('P', 'E'), ('B', 'E')]:
         line_style = '--'
    ax.plot(x, y, z, color='#1f77b4', linewidth=2, linestyle=line_style)

# Plot points
for name, p in pts.items():
    ax.scatter(*p, color='red', s=50)
    # Adjust text position slightly
    ax.text(p[0]+0.15, p[1]+0.15, p[2]+0.1, name, fontsize=14, fontweight='bold')

# Add coordinate axes based on EA, EB, EP
ax.quiver(0,0,0, 2,0,0, color='black', arrow_length_ratio=0.1)
ax.text(2.2, 0, 0, 'x', fontsize=14)
ax.quiver(0,0,0, 0,2,0, color='black', arrow_length_ratio=0.1)
ax.text(0, 2.2, 0, 'y', fontsize=14)
ax.quiver(0,0,0, 0,0,2.5, color='black', arrow_length_ratio=0.1)
ax.text(0, 0, 2.7, 'z', fontsize=14)

# Plane normal vector indication (approximate)
ax.quiver(0, 0.5, 1, -1, 1, 1.5, color='green', linestyle=':', arrow_length_ratio=0.1)
ax.text(-1, 1.5, 2.5, '距离 d', fontsize=12, color='green')

ax.set_title('【典例精讲】空间直角坐标系建模与点到平面的距离', fontsize=16, pad=20)
ax.view_init(elev=20, azim=-60)
ax.axis('off')

os.makedirs('/Users/yangyake/IdeaProjects/math/handouts/images', exist_ok=True)
plt.savefig('/Users/yangyake/IdeaProjects/math/handouts/images/solid_geo_coords.png', dpi=300, bbox_inches='tight')
print("Image saved.")

