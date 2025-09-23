s = str(input("Введіть речення: "))

result = []
for char in s:
    if char.isalpha():
        result.append(str(ord(char)))
    else:
        result.append(char)

print("Після заміни літер на ASCII коди: ", " ".join(result))