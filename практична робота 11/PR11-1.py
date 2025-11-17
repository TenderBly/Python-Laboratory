import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Отримання шляху до папки, де знаходиться скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))
# Формування повного шляху до файлу CSV
csv_path = os.path.join(script_dir, 'comptagevelo2009.csv')

# Завантаження даних
df = pd.read_csv(csv_path)

# Очищення даних - видалення порожніх колонок
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Перетворення дати у правильний формат
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Заповнення пропущених значень нулями
df = df.fillna(0)

# Перетворення числових колонок у правильний тип
numeric_cols = ['Berri1', 'Maisonneuve_1', 'Maisonneuve_2', 'Brébeuf']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

print("=" * 60)
print("1. ПЕРЕГЛЯД ПЕРШИХ РЯДКІВ ДАТАФРЕЙМУ")
print("=" * 60)
print(df.head())

print("\n" + "=" * 60)
print("2. ІНФОРМАЦІЯ ПРО ДАТАФРЕЙМ")
print("=" * 60)
print(df.info())

print("\n" + "=" * 60)
print("3. СТАТИСТИЧНИЙ ОПИС ДАНИХ")
print("=" * 60)
print(df.describe())

# Загальна кількість велосипедистів за рік на всіх велодоріжках
total_all = df[numeric_cols].sum().sum()
print("\n" + "=" * 60)
print("4. ЗАГАЛЬНА КІЛЬКІСТЬ ВЕЛОСИПЕДИСТІВ ЗА РІК НА ВСІХ ВЕЛОДОРІЖКАХ")
print("=" * 60)
print(f"Всього велосипедистів: {total_all:,.0f}")

# Загальна кількість велосипедистів за рік на кожній велодоріжці
print("\n" + "=" * 60)
print("5. ЗАГАЛЬНА КІЛЬКІСТЬ ВЕЛОСИПЕДИСТІВ НА КОЖНІЙ ВЕЛОДОРІЖЦІ")
print("=" * 60)
for col in numeric_cols:
    total = df[col].sum()
    print(f"{col}: {total:,.0f}")

# Додавання колонки місяця
df['Month'] = df['Date'].dt.month
df['MonthName'] = df['Date'].dt.month_name()

# Найпопулярніший місяць для кожної велодоріжки (вибираємо перші три)
print("\n" + "=" * 60)
print("6. НАЙПОПУЛЯРНІШИЙ МІСЯЦЬ ДЛЯ КОЖНОЇ ВЕЛОДОРІЖКИ")
print("=" * 60)

bikes_to_analyze = ['Berri1', 'Maisonneuve_1', 'Maisonneuve_2']

for bike in bikes_to_analyze:
    monthly = df.groupby('Month')[bike].sum()
    max_month_num = monthly.idxmax()
    max_count = monthly.max()
    month_names = {1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень', 
                   5: 'Травень', 6: 'Червень', 7: 'Липень', 8: 'Серпень',
                   9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'}
    print(f"{bike}: {month_names[max_month_num]} ({max_count:,.0f} велосипедистів)")

# Побудова графіка завантаженості велодоріжки Berri1 по місяцям
print("\n" + "=" * 60)
print("7. ГРАФІК ЗАВАНТАЖЕНОСТІ ВЕЛОДОРІЖКИ BERRI1 ПО МІСЯЦЯМ")
print("=" * 60)

monthly_berri = df.groupby('Month')['Berri1'].sum()

plt.figure(figsize=(12, 6))
plt.bar(monthly_berri.index, monthly_berri.values, color='steelblue', edgecolor='navy')
plt.xlabel('Місяць', fontsize=12, weight='bold')
plt.ylabel('Кількість велосипедистів', fontsize=12, weight='bold')
plt.title('Завантаженість велодоріжки Berri1 по місяцям (2009 рік)', 
          fontsize=14, weight='bold', pad=20)
plt.xticks(range(1, 13), 
           ['Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер', 
            'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру'])
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Додавання значень на стовпчики
for i, v in enumerate(monthly_berri.values):
    plt.text(i + 1, v + 1000, f'{v:,.0f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

print("\nГрафік побудовано успішно!")