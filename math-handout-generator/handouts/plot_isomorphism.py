import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib

# Set font for Chinese characters
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'PingFang SC']
matplotlib.rcParams['axes.unicode_minus'] = False

x = np.linspace(1.001, 3, 500)
y = np.log(x - 1) + 2 * np.sqrt(3 - x)

plt.figure(figsize=(8, 6))
plt.plot(x, y, label=r'$f(x) = \ln(x-1) + 2\sqrt{3-x}$', color='#1f77b4', linewidth=2)
plt.axhline(0, color='black', linewidth=1)
plt.axvline(1, color='red', linestyle='--', label=r'渐近线 $x=1$')

# Tangent line at x=2
plt.plot(2, 2, 'ro')
plt.annotate('切点 (2, 2)', xy=(2, 2), xytext=(2.2, 2.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
             fontsize=12)
plt.axhline(2, color='green', linestyle=':', label='切线 $y=2$')

# The zero point (approximate via numpy)
zero_idx = np.argmin(np.abs(y[x < 2]))
zero_x = x[zero_idx]

plt.plot(zero_x, 0, 'go')
plt.annotate(f'唯一零点 $x \\approx {zero_x:.2f}$', xy=(zero_x, 0), xytext=(zero_x + 0.3, -1.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
             fontsize=12)

plt.title('【典例精讲】原题函数图象分析 (a=1)', fontsize=14, pad=15)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.xlim(0.8, 3.2)
plt.ylim(-4, 3)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)

os.makedirs('/Users/yangyake/IdeaProjects/math/handouts/images', exist_ok=True)
plt.savefig('/Users/yangyake/IdeaProjects/math/handouts/images/isomorphism_original.png', dpi=300, bbox_inches='tight')
print("Image saved successfully.")

