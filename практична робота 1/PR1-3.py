n = int(input("Введіть число від 2 до 8: "))

# Верхня частина рисунка
for i in range(1, n + 1):
    print(str(n) * i)

# Нижня частина рисунка
for i in range(n - 1, 0, -1):
    print(str(n) * i)