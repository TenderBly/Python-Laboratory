import numpy as np
import matplotlib.pyplot as plt

x1 = np.linspace(-2, -0.01, 2000)
x2 = np.linspace(0.01, 2, 2000)
x = np.concatenate([x1, x2])

y = np.sin(x) * (1/x) * np.cos(x**2 + 1/x)

plt.figure(figsize=(12, 7))
plt.plot(x, y, 
         linestyle='-',
         color='blue',
         linewidth=2,
         label='Y(x) = sin(x)·(1/x)·cos(x²+1/x)')

plt.xlabel('x', fontsize=12)
plt.ylabel('Y(x)', fontsize=12)

plt.title('Графік функції Y(x) = sin(x)·(1/x)·cos(x²+1/x)', fontsize=14, fontweight='bold')

plt.xlim(-2, 2)
plt.ylim(-1.5, 1.5)

plt.grid(True, alpha=0.3)

plt.legend(loc='best', fontsize=10)

plt.axhline(y=0, color='black', linewidth=0.5)
plt.axvline(x=0, color='black', linewidth=0.5)

plt.tight_layout()
plt.show()