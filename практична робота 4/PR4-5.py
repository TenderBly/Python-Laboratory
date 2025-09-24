import random

def common_in_both():
    n = int(input('Введіть кількість елементів множини A: '))
    m = int(input('Введіть кількість елементів множини B: '))
    lo = int(input('Введіть мінімальне значення (включно): '))
    hi = int(input('Введіть максимальне значення (включно): '))

    A = set()
    B = set()
    while len(A) < n:
        A.add(random.randint(lo, hi))
    while len(B) < m:
        B.add(random.randint(lo, hi))

    print('Множина A:', A)
    print('Множина B:', B)

    result = A & B
    if result:
        print('Спільні елементи (перетин):', result)
    else:
        print('Спільних елементів немає.')

    return result

common_in_both()
