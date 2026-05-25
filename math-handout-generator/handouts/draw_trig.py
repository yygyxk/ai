import matplotlib.pyplot as plt
import os
import math

os.makedirs('/Users/yangyake/IdeaProjects/math/handouts/images', exist_ok=True)

def draw_tri(filename, A, B, C, labels, alt_point=None, alt_label=None):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', lw=1.5)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', lw=1.5)
    ax.plot([C[0], A[0]], [C[1], A[1]], 'k-', lw=1.5)

    if alt_point:
        ax.plot([A[0], alt_point[0]], [A[1], alt_point[1]], 'k--', lw=1)
        ax.plot([B[0], alt_point[0]], [B[1], alt_point[1]], 'k--', lw=1)
        ax.text(alt_point[0], alt_point[1]-0.4, alt_label, fontsize=12, ha='center')

    ax.text(A[0]-0.3, A[1]-0.3, labels[0], fontsize=12, ha='right')
    ax.text(B[0]+0.3, B[1]-0.3, labels[1], fontsize=12, ha='left')
    ax.text(C[0], C[1]+0.3, labels[2], fontsize=12, ha='center')

    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f'/Users/yangyake/IdeaProjects/math/handouts/images/{filename}', dpi=300)
    plt.close()

# Original
draw_tri('trig_original.png', (0,0), (2,0), (8,6), ['A', 'B', 'C'], (1,-1), 'D')
# V1: generic
draw_tri('trig_var1.png', (0,0), (5,0), (2, 3.464), ['C', 'A', 'B'])

# V4: A=60, b=2, c=3. D is midpoint of BC.
A = (0,0)
C = (2,0)
B = (3*math.cos(math.pi/3), 3*math.sin(math.pi/3))
D = ((B[0]+C[0])/2, (B[1]+C[1])/2)
fig, ax = plt.subplots(figsize=(4,3))
ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=1.5)
ax.plot([A[0], D[0]], [A[1], D[1]], 'k--', lw=1)
ax.text(A[0]-0.2, A[1]-0.2, 'A', fontsize=12)
ax.text(B[0], B[1]+0.2, 'B', fontsize=12)
ax.text(C[0]+0.2, C[1]-0.2, 'C', fontsize=12)
ax.text(D[0]+0.2, D[1], 'D', fontsize=12)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig('/Users/yangyake/IdeaProjects/math/handouts/images/trig_var4.png', dpi=300)
plt.close()

