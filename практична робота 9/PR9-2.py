import json
import os
from datetime import time

# ====== ФАЙЛИ ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(BASE_DIR, "trains.json")              # вихідний (не змінюємо)
RESULT_FILE = os.path.join(BASE_DIR, "trains_at_station.json")   # робочий (усі зміни сюди)


# ====== ДОПОМІЖНІ ФУНКЦІЇ ======
def load_data():
    """Завантажує дані з основного або результатного файлу, якщо вони не порожні"""
    # спроба відкрити результатний файл
    if os.path.exists(RESULT_FILE) and os.path.getsize(RESULT_FILE) > 0:
        try:
            with open(RESULT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Файл trains_at_station.json пошкоджений або порожній. Використовую вихідні дані.")
    
    # якщо результатного нема або він пустий
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """Записує дані у результатний файл (trains_at_station.json)"""
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def show_data(data):
    """Виводить вміст даних"""
    if not data:
        print("Дані відсутні.")
    else:
        print("\n--- ПОТОЧНІ ДАНІ ---")
        for t in data:
            print(f"Поїзд №{t['number']}: {t['route']}, "
                  f"прибуття {t['arrival']['hour']:02d}:{t['arrival']['minute']:02d}, "
                  f"відправлення {t['departure']['hour']:02d}:{t['departure']['minute']:02d}")


# ====== ОСНОВНІ ОПЕРАЦІЇ ======
def add_train(data):
    """Додає новий запис"""
    number = input("Номер поїзда: ")
    route = input("Маршрут (звідки – куди): ")
    arrival_hour = int(input("Година прибуття (0–23): "))
    arrival_min = int(input("Хвилини прибуття (0–59): "))
    departure_hour = int(input("Година відправлення (0–23): "))
    departure_min = int(input("Хвилини відправлення (0–59): "))

    train = {
        "number": number,
        "route": route,
        "arrival": {"hour": arrival_hour, "minute": arrival_min},
        "departure": {"hour": departure_hour, "minute": departure_min}
    }
    data.append(train)
    save_data(data)
    print("✅ Запис додано у trains_at_station.json!")


def delete_train(data):
    """Видаляє запис за номером"""
    num = input("Введіть номер поїзда для видалення: ")
    new_data = [t for t in data if t["number"] != num]
    if len(new_data) < len(data):
        save_data(new_data)
        print("🚆 Запис видалено з trains_at_station.json.")
    else:
        print("❌ Поїзд не знайдено.")


def search_train(data):
    """Пошук по маршруту"""
    route = input("Введіть напрям (або частину назви): ").lower()
    found = [t for t in data if route in t["route"].lower()]
    if found:
        print("\n🔎 Знайдені поїзди:")
        show_data(found)
        save_data(found)
        print("✅ Результати пошуку записано у trains_at_station.json.")
    else:
        print("Нічого не знайдено.")


def trains_at_time(data):
    """Знаходить поїзди, що стоять на станції у певний момент часу"""
    hour = int(input("Година (0–23): "))
    minute = int(input("Хвилина (0–59): "))
    current = time(hour, minute)

    standing = []
    for t in data:
        arrival = time(t["arrival"]["hour"], t["arrival"]["minute"])
        departure = time(t["departure"]["hour"], t["departure"]["minute"])
        if arrival <= current <= departure:
            standing.append(t)

    if standing:
        print("\n🚉 На станції зараз стоять:")
        show_data(standing)
    else:
        print("На станції зараз немає поїздів.")

    save_data(standing)
    print("✅ Результати записано у trains_at_station.json.")


# ====== МЕНЮ ======
def main():
    data = load_data()
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Показати всі записи")
        print("2. Додати запис")
        print("3. Видалити запис")
        print("4. Пошук за маршрутом")
        print("5. Визначити поїзди, що стоять на станції")
        print("0. Вихід")

        choice = input("Ваш вибір: ")
        if choice == "1":
            show_data(data)
        elif choice == "2":
            add_train(data)
            data = load_data()
        elif choice == "3":
            delete_train(data)
            data = load_data()
        elif choice == "4":
            search_train(data)
        elif choice == "5":
            trains_at_time(data)
        elif choice == "0":
            print("Вихід із програми.")
            break
        else:
            print("Невірний вибір!")


if __name__ == "__main__":
    main()
