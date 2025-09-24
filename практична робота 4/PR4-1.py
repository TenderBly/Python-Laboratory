n = int(input("Введіть розмір масиву n = "))

print(f"Введіть {n} елементів масиву:")
arr = [int(input()) for _ in range(n)]

print("Оригінальний масив: ", arr)

print("Масив у зворотному порядку: ", arr[::-1])

reversed_arr = []
for i in range(n-1, -1, -1):
    reversed_arr.append(arr[i])