# Програма для роботи з текстовими файлами TF23_1 та TF23_2

import os
# Встановлюємо робочу директорію там, де знаходиться скрипт
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Завдання а) Створюємо файл TF23_1 із рядків різної довжини
print("Створюємо файл TF23_1...")

try:
    file = open('TF23_1.txt', 'w', encoding='utf-8')
    file.write("  Програмування  \n")
    file.write("  10101  \n")
    file.write("  Тест  \n")
    file.write("  111000111  \n")
    file.write("  Обробка файлів  \n")
    file.write("  0101010101  \n")
    file.write("  Python  \n")
    file.write("  1  \n")
    file.write("  Довгий рядок 010101  \n")
    file.write("  Кінець 100  \n")
    file.close()
    print("Файл TF23_1.txt створено!")
except:
    print("Помилка при створенні файлу TF23_1!")


# Завдання б) Читаємо TF23_1, замінюємо 1 на 0 і навпаки, записуємо в TF23_2
print("\nОбробляємо файл TF23_1 та створюємо TF23_2...")

try:
    file1 = open('TF23_1.txt', 'r', encoding='utf-8')
    text = file1.read()
    file1.close()
    
    # Замінюємо символи
    new_text = ""
    for i in range(len(text)):
        if text[i] == '1':
            new_text = new_text + '0'
        elif text[i] == '0':
            new_text = new_text + '1'
        else:
            new_text = new_text + text[i]
    
    # Видаляємо переноси рядків
    new_text = new_text.replace('\n', '')
    
    # Записуємо в TF23_2 по 15 символів у рядок
    file2 = open('TF23_2.txt', 'w', encoding='utf-8')
    i = 0
    while i < len(new_text):
        line = new_text[i:i+15]
        file2.write(line + '\n')
        i = i + 15
    file2.close()
    
    print("Файл TF23_2.txt створено!")
except:
    print("Помилка при обробці файлу!")


# Завдання в) Читаємо та друкуємо вміст TF23_2
print("\nЧитаємо файл TF23_2:\n")

try:
    file3 = open('TF23_2.txt', 'r', encoding='utf-8')
    lines = file3.readlines()
    file3.close()
    
    for i in range(len(lines)):
        print("Рядок", i+1, ":", lines[i].strip())
    
    print("\nГотово!")
except:
    print("Помилка при читанні файлу TF23_2!")