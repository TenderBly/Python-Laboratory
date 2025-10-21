import csv
import os

# Поточна директорія
current_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(current_dir, "Exports of goods and services (% of GDP)15and19.csv")
output_file = os.path.join(current_dir, "filtered_exports.csv")

try:
    # Визначаємо роздільник (',' або ';')
    with open(input_file, 'r', encoding='utf-8') as f:
        sample = f.read(1024)
        delimiter = ';' if sample.count(';') > sample.count(',') else ','

    # Зчитуємо файл
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        data = list(reader)

        # Перевіримо, які саме колонки є
        print("Колонки у файлі:", reader.fieldnames)

        # Знайдемо колонки, які містять 2015 і 2019
        col_2015 = next((c for c in reader.fieldnames if "2015" in c), None)
        col_2019 = next((c for c in reader.fieldnames if "2019" in c), None)

        if not col_2015 or not col_2019:
            raise KeyError("Не знайдено колонки для 2015 або 2019 року")

        print("\nВміст файлу:\n")
        for row in data:
            print(row)

        # Введення діапазону
        print("\nВведіть діапазон для пошуку даних (у % ВВП):")
        lower = float(input("Мінімальне значення: "))
        upper = float(input("Максимальне значення: "))

        filtered = []
        for row in data:
            try:
                val_2015 = float(row[col_2015]) if row[col_2015] else None
                val_2019 = float(row[col_2019]) if row[col_2019] else None
            except ValueError:
                continue

            if (val_2015 and lower <= val_2015 <= upper) or (val_2019 and lower <= val_2019 <= upper):
                filtered.append(row)

        # Запис у новий файл
        if filtered:
            with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
                writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(filtered)
            print(f"\n✅ Результати збережено у файл: {output_file}")
        else:
            print("\n⚠️ Дані у вказаному діапазоні не знайдені.")

except FileNotFoundError:
    print(f"❌ Помилка: файл '{os.path.basename(input_file)}' не знайдено!")
except Exception as e:
    print(f"⚠️ Сталася помилка при обробці файлу: {e}")
