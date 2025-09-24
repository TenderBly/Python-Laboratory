def shortest_word():
    A = list(input('Введіть список слів: ').split())

    print('Оригінальний список:', A)

    shortest = min(A, key=len)

    print('Найкоротше слово із списку:', shortest)

    return shortest
shortest_word()
