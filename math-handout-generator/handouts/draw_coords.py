import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Coordinates in math system:
# E=(0,0,0)
# A=(0,-1,0)
# D=(0,3,0)
# B=(1,0,0)
# C=(1,2,0)
# P=(0,0,2)

# For plotting, map to visually appealing axes
# Math X (EB direction) -> Matplotlib X
# Math Y (AD direction) -> Matplotlib Y
# Math Z (EP direction) -> Matplotlib Z
A = np.array([0, -1, 0])
E = np.array([0, 0, 0])
D = np.array([0, 3, 0])
B = np.array([1, 0, 0])
C = np.array([1, 2, 0])
P = np.array([0, 0, 2])
F = (P + B) / 2

points = {'A': A, 'E': E, 'D': D, 'B': B, 'C': C, 'P': P, 'F': F}

# Edges (start, end, style, color)
edges = [
    ('P', 'A', '-', 'k'),
    ('P', 'B', '-', 'k'),
    ('P', 'C', '-', 'k'),
    ('P', 'D', '-', 'k'),
    ('A', 'B', '-', 'k'),
    ('B', 'C', '-', 'k'),
    ('C', 'D', '-', 'k'),
    ('A', 'D', '--', 'k'),
    ('P', 'E', '--', 'k'),
    ('B', 'E', '--', 'k')
]

for start, end, style, color in edges:
    pt1 = points[start]
    pt2 = points[end]
    ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], [pt1[2], pt2[2]], linestyle=style, color=color, linewidth=1.5)

# Plot F
ax.plot([F[0]], [F[1]], [F[2]], 'ko', markersize=4)

# Plot Coordinate Axes
ax.quiver(0, 0, 0, 2, 0, 0, color='r', arrow_length_ratio=0.1, linestyle='-.') # X-axis
ax.quiver(0, 0, 0, 0, 4, 0, color='g', arrow_length_ratio=0.1, linestyle='-.') # Y-axis
ax.quiver(0, 0, 0, 0, 0, 2.5, color='b', arrow_length_ratio=0.1, linestyle='-.') # Z-axis

ax.text(2.1, 0, 0, 'x', color='r', fontsize=12)
ax.text(0, 4.1, 0, 'y', color='g', fontsize=12)
ax.text(0, 0, 2.6, 'z', color='b', fontsize=12)

# Labels
for name, pt in points.items():
    if name == 'P':
        ax.text(pt[0], pt[1], pt[2]+0.1, name, fontsize=12, ha='center')
    elif name == 'A':
        ax.text(pt[0], pt[1]-0.2, pt[2], name, fontsize=12, ha='right')
    elif name == 'D':
        ax.text(pt[0], pt[1]+0.2, pt[2], name, fontsize=12, ha='left')
    elif name == 'B':
        ax.text(pt[0]+0.1, pt[1], pt[2]-0.1, name, fontsize=12, ha='left')
    elif name == 'C':
        ax.text(pt[0]+0.1, pt[1]+0.1, pt[2], name, fontsize=12, ha='left')
    elif name == 'E':
        ax.text(pt[0]-0.1, pt[1]-0.1, pt[2], name, fontsize=12, ha='right')
    elif name == 'F':
        ax.text(pt[0]+0.1, pt[1], pt[2], name, fontsize=12, ha='left')

ax.set_axis_off()
ax.view_init(elev=20, azim=30)
plt.tight_layout()
plt.savefig('images/teacher_coords.png', dpi=300)
plt.close()

