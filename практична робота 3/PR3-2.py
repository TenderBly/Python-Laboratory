word = input("Введіть слово, записане кирилицею: ")

latin_substitutes = ['i', 'a', 'o', 'I', 'A', 'O']

has_substitution = False
for char in word:
    if char in latin_substitutes:
        has_substitution = True
        break

if has_substitution:
    print("Слово містить підміну кириличних літер на латинські")
else:
    print("Слово не містить підміни кириличних літер на латинські")