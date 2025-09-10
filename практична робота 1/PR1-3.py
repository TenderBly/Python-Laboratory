while True:
    n = int(input("Введіть число від 1 до 9: "))
    if n < 1 or n > 9:
        print("Число повинно бути від 1 до 9!")
    else:
        for i in range(n, 0, -1):
            print(str(n) * i)

        for i in range(2, n + 1):
            print(str(n) * i)
        
        break