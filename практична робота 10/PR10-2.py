import matplotlib.pyplot as plt

categories = ['Смартфони', 'Ноутбуки', 'Планшети', 'Навушники', 'Аксесуари']
sales = [450, 380, 220, 150, 180]

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

plt.figure(figsize=(10, 8))

plt.pie(sales, 
        labels=categories, 
        colors=colors,
        autopct='%1.1f%%',  
        startangle=90,       
        explode=(0.1, 0, 0, 0, 0))  

plt.title('Розподіл продажів товарів у магазині електроніки\n(Березень 2025)', 
          fontsize=16, 
          fontweight='bold',
          pad=20)

legend_labels = [f'{cat}: {val} тис. грн' for cat, val in zip(categories, sales)]
plt.legend(legend_labels, 
          loc='upper left', 
          bbox_to_anchor=(1, 1),
          fontsize=10)

plt.axis('equal')

plt.tight_layout()

plt.show()

total_sales = sum(sales)
print(f"\nЗагальний обсяг продажів: {total_sales} тис. грн")
print("\nДетальна статистика:")
for cat, val in zip(categories, sales):
    percentage = (val / total_sales) * 100
    print(f"{cat}: {val} тис. грн ({percentage:.1f}%)")