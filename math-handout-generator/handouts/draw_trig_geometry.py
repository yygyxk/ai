import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
import os

os.makedirs('/Users/yangyake/IdeaProjects/math/handouts/images', exist_ok=True)

def draw_right_angle(ax, pt, v1, v2, size=0.05):
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    p1 = pt + v1 * size
    p2 = pt + v1 * size + v2 * size
    p3 = pt + v2 * size
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], 'k-', lw=1)

def draw_original_problem():
    fig, ax = plt.subplots(figsize=(4, 5))
    A = np.array([0, 0])
    B = np.array([0.75, 0])
    C = np.array([0.75, 0.866])
    D = np.array([0, 0.866])
    E = np.array([0.5, 0.866])
    F = np.array([0.75, 0.433])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=1.5)
    ax.plot([A[0], E[0]], [A[1], E[1]], 'k-', lw=1.5)
    ax.plot([A[0], F[0]], [A[1], F[1]], 'k-', lw=1.5)
    ax.plot([E[0], F[0]], [E[1], F[1]], 'k-', lw=1.5)

    ax.text(A[0]-0.05, A[1]-0.05, 'A', fontsize=14)
    ax.text(B[0]+0.02, B[1]-0.05, 'B', fontsize=14)
    ax.text(C[0]+0.02, C[1]+0.02, 'C', fontsize=14)
    ax.text(D[0]-0.05, D[1]+0.02, 'D', fontsize=14)
    ax.text(E[0]-0.02, E[1]+0.02, 'E', fontsize=14)
    ax.text(F[0]+0.02, F[1], 'F', fontsize=14)

    mid_ae = (A + E) / 2
    ax.text(mid_ae[0]-0.06, mid_ae[1]+0.04, '1', fontsize=14)

    arc1 = Arc(A, 0.3, 0.3, angle=0, theta1=np.degrees(np.arctan2(F[1], F[0])), theta2=np.degrees(np.arctan2(E[1], E[0])), color='k')
    arc2 = Arc(A, 0.3, 0.3, angle=0, theta1=0, theta2=np.degrees(np.arctan2(F[1], F[0])), color='k')
    ax.add_patch(arc1)
    ax.add_patch(arc2)

    # Adjust position for 'x'
    ax.text(0.12, 0.15, 'x', fontsize=12)
    ax.text(0.18, 0.05, 'x', fontsize=12)

    draw_right_angle(ax, F, A-F, E-F, 0.04)

    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig('/Users/yangyake/IdeaProjects/math/handouts/images/trig_original.png', dpi=300, bbox_inches='tight')
    plt.close()

def draw_half_angle_proof():
    fig, ax = plt.subplots(figsize=(3, 5))
    C = np.array([0, 0])
    B = np.array([4, 0])
    A = np.array([0, 3])
    D = np.array([0, 8])

    ax.plot([C[0], B[0]], [C[1], B[1]], 'k-', lw=1.5)
    ax.plot([D[0], C[0]], [D[1], C[1]], 'k-', lw=1.5)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', lw=1.5)
    ax.plot([D[0], B[0]], [D[1], B[1]], 'k-', lw=1.5)

    ax.text(C[0]-0.5, C[1]-0.1, 'C', fontsize=14)
    ax.text(B[0]+0.1, B[1]-0.1, 'B', fontsize=14)
    ax.text(A[0]-0.5, A[1], 'A', fontsize=14)
    ax.text(D[0]-0.5, D[1], 'D', fontsize=14)

    draw_right_angle(ax, C, B-C, A-C, 0.4)

    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig('/Users/yangyake/IdeaProjects/math/handouts/images/trig_var4.png', dpi=300, bbox_inches='tight')
    plt.close()

def draw_zhao_shuang():
    fig, ax = plt.subplots(figsize=(5, 5))
    A, B, C, D = np.array([0,4]), np.array([3,0]), np.array([7,3]), np.array([4,7])
    E, F, G, H = np.array([4,4]), np.array([3,4]), np.array([3,3]), np.array([4,3])

    # Outer
    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=1.5)
    # Inner
    ax.plot([E[0], F[0], G[0], H[0], E[0]], [E[1], F[1], G[1], H[1], E[1]], 'k-', lw=1.5)

    # Lines forming triangles
    ax.plot([A[0], E[0]], [A[1], E[1]], 'k-', lw=1.5)
    ax.plot([B[0], F[0]], [B[1], F[1]], 'k-', lw=1.5)
    ax.plot([C[0], G[0]], [C[1], G[1]], 'k-', lw=1.5)
    ax.plot([D[0], H[0]], [D[1], H[1]], 'k-', lw=1.5)

    ax.text(A[0]-0.3, A[1], 'A', fontsize=14)
    ax.text(B[0], B[1]-0.3, 'B', fontsize=14)
    ax.text(C[0]+0.1, C[1], 'C', fontsize=14)
    ax.text(D[0], D[1]+0.1, 'D', fontsize=14)

    ax.text(E[0]-0.1, E[1]+0.1, 'E', fontsize=12)
    ax.text(F[0]-0.2, F[1]-0.1, 'F', fontsize=12)
    ax.text(G[0]+0.1, G[1]-0.2, 'G', fontsize=12)
    ax.text(H[0]+0.1, H[1]+0.1, 'H', fontsize=12)

    draw_right_angle(ax, E, A-E, D-E, 0.3)
    draw_right_angle(ax, F, B-F, A-F, 0.3)
    draw_right_angle(ax, G, C-G, B-G, 0.3)
    draw_right_angle(ax, H, D-H, C-H, 0.3)

    # Angle theta in triangle AFB
    arc = Arc(A, 1.2, 1.2, angle=0, theta1=np.degrees(np.arctan2(F[1]-A[1], F[0]-A[0])), theta2=np.degrees(np.arctan2(B[1]-A[1], B[0]-A[0])), color='k')
    ax.add_patch(arc)
    ax.text(0.7, 3.2, r'$\theta$', fontsize=14)

    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig('/Users/yangyake/IdeaProjects/math/handouts/images/trig_test3.png', dpi=300, bbox_inches='tight')
    plt.close()

draw_original_problem()
draw_half_angle_proof()
draw_zhao_shuang()

