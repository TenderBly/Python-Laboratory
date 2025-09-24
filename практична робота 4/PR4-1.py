n = int(input("Введіть розмір масиву n = "))

print(f"Введіть {n} елементів масиву:")
arr = [int(input()) for _ in range(n)]

print("Оригінальний масив:", arr)

reversed_arr = arr.copy()
reversed_arr.reverse()

print("Масив у зворотному порядку:", reversed_arr)