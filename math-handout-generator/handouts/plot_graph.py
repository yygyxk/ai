import os
try:
    import matplotlib
    matplotlib.use('Agg') # 解决 macOS 下可能没有 GUI 后端的报错
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    os.system('pip3 install matplotlib numpy')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

# 支持中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def f(x):
    return (x - 2) * np.exp(x) + (x - 1)**2

x = np.linspace(-2.5, 2.2, 500)
y = f(x)

plt.figure(figsize=(9, 5))
plt.plot(x, y, 'b-', linewidth=2.5, label=r'$f(x) = (x-2)e^x + (x-1)^2$ (设 a=1 时的示意图)')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)

# 大致估算根的位置
x1_approx, x2_approx = -1.59, 1.25
plt.scatter([x1_approx, x2_approx], [0, 0], color='red', s=60, zorder=5)
plt.text(x1_approx - 0.2, 0.4, r'$x_1$', fontsize=15, color='red', fontweight='bold')
plt.text(x2_approx + 0.1, 0.4, r'$x_2$', fontsize=15, color='red', fontweight='bold')

# 极小值点
plt.scatter([1], [f(1)], color='green', s=60, zorder=5)
plt.text(1.1, f(1) + 0.2, r'极小值点 $x=1$', fontsize=14, color='green')
plt.axvline(1, color='gray', linestyle='--', label=r'对称中轴参考线 $x=1$')

# 标注偏移量
plt.annotate('', xy=(x1_approx, -1), xytext=(1, -1), arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
plt.text((x1_approx+1)/2 - 0.6, -0.8, r'距离更远', color='purple', fontsize=12)

plt.annotate('', xy=(1, -1), xytext=(x2_approx, -1), arrowprops=dict(arrowstyle='<->', color='orange', lw=2))
plt.text((1+x2_approx)/2 - 0.4, -0.8, r'距离更近', color='orange', fontsize=12)

plt.ylim(-4, 5)
plt.xlim(-3, 2.5)
plt.legend(fontsize=12)
plt.title('【变式6】 2016全国I卷理科压轴题 极值点偏移现象', fontsize=16)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

os.makedirs('/Users/yangyake/IdeaProjects/math/handouts/images', exist_ok=True)
plt.savefig('/Users/yangyake/IdeaProjects/math/handouts/images/2016_math_var6.png', dpi=300)
print("Image generated successfully at /Users/yangyake/IdeaProjects/math/handouts/images/2016_math_var6.png")

