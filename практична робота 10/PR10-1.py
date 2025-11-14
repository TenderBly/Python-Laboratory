import matplotlib.pyplot as plt

# --- Дані з World Bank (Children out of school, primary) ---
years = list(range(2003, 2024))

# Україна (Children out of school, primary)
ukraine = [25000, 23000, 21000, 20000, 18000, 15000, 12000, 11000, 10000, 9500,
           9000, 8500, 8300, 8000, 7800, 7600, 7500, 7400, 7300, 7200, 7100]

# США (Children out of school, primary)
usa = [300000, 295000, 290000, 285000, 280000, 275000, 270000, 260000, 250000, 245000,
       240000, 230000, 225000, 220000, 215000, 210000, 205000, 200000, 190000, 180000, 175000]

plt.figure(figsize=(10, 6))
plt.plot(years, ukraine, color='blue', linewidth=2.5, label='Україна', linestyle='-')
plt.plot(years, usa, color='red', linewidth=2.5, label='США', linestyle='--')

plt.title("Children out of school, primary (2003–2023)", fontsize=14)
plt.xlabel("Рік", fontsize=12)
plt.ylabel("Кількість дітей (осіб)", fontsize=12)
plt.xticks(years, rotation=45) 
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

country = input("Введіть назву країни (Україна або США): ").strip().lower()

plt.figure(figsize=(10, 6))
if country == "україна":
    plt.bar(years, ukraine, color='blue')
    plt.title("Діти, які не відвідують школу (Україна, 2003–2023)", fontsize=14)
    plt.ylabel("Кількість дітей (осіб)")
elif country == "сша":
    plt.bar(years, usa, color='red')
    plt.title("Children out of school, primary (USA, 2003–2023)", fontsize=14)
    plt.ylabel("Number of children (persons)")
else:
    print("Країну не розпізнано! Введіть 'Україна' або 'США'.")
    exit()

plt.xlabel("Рік")
plt.xticks(years, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
