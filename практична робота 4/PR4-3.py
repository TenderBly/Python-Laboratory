def convert():
    A = list(map(float, input('Введіть список дійсних чисел: ').split()))
    print('Оригінальний список: ', A)

    result = []
    for x in A:
        result.append(round(x))

    print('Сконвертований список: ', result)
    return result

convert()
