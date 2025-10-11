"""
Програма для роботи з розкладом поїздів на станції
Варіант: визначення поїздів, які стоять на станції у визначений момент часу
"""

# Початковий словник з розкладом поїздів
trains_schedule = {
    "701К": {
        "призначення": "Київ - Харків",
        "прибуття": {"година": 8, "хвилина": 15},
        "відправлення": {"година": 8, "хвилина": 45},
        "тип": "швидкий"
    },
    "145Л": {
        "призначення": "Львів - Одеса",
        "прибуття": {"година": 10, "хвилина": 30},
        "відправлення": {"година": 11, "хвилина": 10},
        "тип": "пасажирський"
    },
    "89Д": {
        "призначення": "Дніпро - Київ",
        "прибуття": {"година": 14, "хвилина": 20},
        "відправлення": {"година": 14, "хвилина": 50},
        "тип": "експрес"
    },
    "234П": {
        "призначення": "Полтава - Харків",
        "прибуття": {"година": 9, "хвилина": 5},
        "відправлення": {"година": 9, "хвилина": 25},
        "тип": "приміський"
    },
    "567З": {
        "призначення": "Запоріжжя - Львів",
        "прибуття": {"година": 16, "хвилина": 40},
        "відправлення": {"година": 17, "хвилина": 15},
        "тип": "пасажирський"
    },
    "892Ч": {
        "призначення": "Чернігів - Одеса",
        "прибуття": {"година": 7, "хвилина": 50},
        "відправлення": {"година": 8, "хвилина": 10},
        "тип": "швидкий"
    },
    "321В": {
        "призначення": "Вінниця - Суми",
        "прибуття": {"година": 12, "хвилина": 0},
        "відправлення": {"година": 12, "хвилина": 35},
        "тип": "пасажирський"
    },
    "456М": {
        "призначення": "Маріуполь - Київ",
        "прибуття": {"година": 15, "хвилина": 25},
        "відправлення": {"година": 16, "хвилина": 5},
        "тип": "швидкий"
    },
    "678Х": {
        "призначення": "Харків - Ужгород",
        "прибуття": {"година": 11, "хвилина": 45},
        "відправлення": {"година": 12, "хвилина": 20},
        "тип": "пасажирський"
    },
    "123І": {
        "призначення": "Івано-Франківськ - Київ",
        "прибуття": {"година": 18, "хвилина": 30},
        "відправлення": {"година": 19, "хвилина": 0},
        "тип": "експрес"
    }
}


def validate_time(hour, minute):
    """Перевірка коректності введеного часу"""
    if not isinstance(hour, int) or not isinstance(minute, int):
        raise ValueError("Година та хвилина повинні бути цілими числами")
    if hour < 0 or hour > 23:
        raise ValueError("Година повинна бути в діапазоні від 0 до 23")
    if minute < 0 or minute > 59:
        raise ValueError("Хвилина повинна бути в діапазоні від 0 до 59")
    return True


def time_to_minutes(hour, minute):
    """Конвертація часу у хвилини для зручності порівняння"""
    return hour * 60 + minute


def format_time(time_dict):
    """Форматування часу для виведення"""
    return f"{time_dict['година']:02d}:{time_dict['хвилина']:02d}"


def display_all_trains(schedule):
    """Виведення на екран всіх значень словника"""
    if not schedule:
        print("\n❌ Розклад порожній!")
        return
    
    print("\n" + "="*80)
    print("📋 РОЗКЛАД ПОЇЗДІВ НА СТАНЦІЇ")
    print("="*80)
    
    for train_number, info in schedule.items():
        print(f"\n🚂 Поїзд №{train_number}")
        print(f"   Маршрут: {info['призначення']}")
        print(f"   Прибуття: {format_time(info['прибуття'])}")
        print(f"   Відправлення: {format_time(info['відправлення'])}")
        print(f"   Тип: {info['тип']}")
    
    print("\n" + "="*80)


def add_train(schedule):
    """Додавання нового запису до словника"""
    print("\n➕ ДОДАВАННЯ НОВОГО ПОЇЗДА")
    print("-" * 40)
    
    try:
        train_number = input("Введіть номер поїзда (наприклад, 701К): ").strip()
        
        if not train_number:
            raise ValueError("Номер поїзда не може бути порожнім")
        
        if train_number in schedule:
            raise ValueError(f"Поїзд з номером {train_number} вже існує в розкладі")
        
        destination = input("Введіть призначення (наприклад, Київ - Харків): ").strip()
        if not destination:
            raise ValueError("Призначення не може бути порожнім")
        
        # Введення часу прибуття
        arrival_hour = int(input("Введіть годину прибуття (0-23): "))
        arrival_minute = int(input("Введіть хвилину прибуття (0-59): "))
        validate_time(arrival_hour, arrival_minute)
        
        # Введення часу відправлення
        departure_hour = int(input("Введіть годину відправлення (0-23): "))
        departure_minute = int(input("Введіть хвилину відправлення (0-59): "))
        validate_time(departure_hour, departure_minute)
        
        # Перевірка, що час відправлення пізніше прибуття
        if time_to_minutes(departure_hour, departure_minute) <= time_to_minutes(arrival_hour, arrival_minute):
            raise ValueError("Час відправлення повинен бути пізніше часу прибуття")
        
        train_type = input("Введіть тип поїзда (швидкий/пасажирський/експрес/приміський): ").strip()
        if not train_type:
            train_type = "пасажирський"
        
        # Додавання поїзда до розкладу
        schedule[train_number] = {
            "призначення": destination,
            "прибуття": {"година": arrival_hour, "хвилина": arrival_minute},
            "відправлення": {"година": departure_hour, "хвилина": departure_minute},
            "тип": train_type
        }
        
        print(f"\n✅ Поїзд {train_number} успішно додано до розкладу!")
        
    except ValueError as e:
        print(f"\n❌ Помилка введення: {e}")
    except Exception as e:
        print(f"\n❌ Непередбачена помилка: {e}")


def delete_train(schedule):
    """Видалення запису зі словника"""
    print("\n➖ ВИДАЛЕННЯ ПОЇЗДА З РОЗКЛАДУ")
    print("-" * 40)
    
    try:
        train_number = input("Введіть номер поїзда для видалення: ").strip()
        
        if not train_number:
            raise ValueError("Номер поїзда не може бути порожнім")
        
        if train_number not in schedule:
            raise KeyError(f"Поїзд з номером {train_number} не знайдено в розкладі")
        
        # Підтвердження видалення
        print(f"\n🚂 Поїзд: {train_number} - {schedule[train_number]['призначення']}")
        confirmation = input("Ви впевнені, що хочете видалити цей поїзд? (так/ні): ").strip().lower()
        
        if confirmation in ['так', 'yes', 'y', 'т']:
            del schedule[train_number]
            print(f"\n✅ Поїзд {train_number} успішно видалено з розкладу!")
        else:
            print("\n❌ Видалення скасовано")
            
    except KeyError as e:
        print(f"\n❌ Помилка: {e}")
    except Exception as e:
        print(f"\n❌ Непередбачена помилка: {e}")


def display_sorted_trains(schedule):
    """Перегляд вмісту словника за відсортованими ключами"""
    if not schedule:
        print("\n❌ Розклад порожній!")
        return
    
    print("\n" + "="*80)
    print("📋 РОЗКЛАД ПОЇЗДІВ (ВІДСОРТОВАНО ЗА НОМЕРОМ)")
    print("="*80)
    
    sorted_keys = sorted(schedule.keys())
    
    for train_number in sorted_keys:
        info = schedule[train_number]
        print(f"\n🚂 Поїзд №{train_number}")
        print(f"   Маршрут: {info['призначення']}")
        print(f"   Прибуття: {format_time(info['прибуття'])}")
        print(f"   Відправлення: {format_time(info['відправлення'])}")
        print(f"   Тип: {info['тип']}")
    
    print("\n" + "="*80)


def find_trains_at_station(schedule):
    """
    Визначення поїздів, які стоять на станції у визначений момент часу
    """
    print("\n🔍 ПОШУК ПОЇЗДІВ НА СТАНЦІЇ")
    print("-" * 40)
    
    try:
        check_hour = int(input("Введіть годину для перевірки (0-23): "))
        check_minute = int(input("Введіть хвилину для перевірки (0-59): "))
        validate_time(check_hour, check_minute)
        
        check_time = time_to_minutes(check_hour, check_minute)
        
        trains_at_station = []
        
        for train_number, info in schedule.items():
            arrival_time = time_to_minutes(
                info['прибуття']['година'],
                info['прибуття']['хвилина']
            )
            departure_time = time_to_minutes(
                info['відправлення']['година'],
                info['відправлення']['хвилина']
            )
            
            # Поїзд на станції, якщо час перевірки між прибуттям та відправленням
            if arrival_time <= check_time <= departure_time:
                trains_at_station.append({
                    'номер': train_number,
                    'призначення': info['призначення'],
                    'прибуття': format_time(info['прибуття']),
                    'відправлення': format_time(info['відправлення'])
                })
        
        print(f"\n⏰ Час перевірки: {check_hour:02d}:{check_minute:02d}")
        print("=" * 60)
        
        if trains_at_station:
            print(f"\n✅ На станції знаходиться {len(trains_at_station)} поїзд(ів):\n")
            for train in trains_at_station:
                print(f"🚂 Поїзд №{train['номер']}")
                print(f"   Маршрут: {train['призначення']}")
                print(f"   Прибув: {train['прибуття']}, відправиться: {train['відправлення']}\n")
        else:
            print("\n❌ У вказаний час на станції немає поїздів")
        
        print("=" * 60)
        
    except ValueError as e:
        print(f"\n❌ Помилка введення: {e}")
    except Exception as e:
        print(f"\n❌ Непередбачена помилка: {e}")


def display_menu():
    """Відображення головного меню"""
    print("\n" + "="*60)
    print("🚉 СИСТЕМА УПРАВЛІННЯ РОЗКЛАДОМ ПОЇЗДІВ")
    print("="*60)
    print("1. Показати всі поїзди")
    print("2. Показати поїзди (відсортовано за номером)")
    print("3. Додати новий поїзд")
    print("4. Видалити поїзд")
    print("5. Знайти поїзди на станції у певний час")
    print("0. Вихід")
    print("="*60)


def main():
    """Головна функція програми з діалоговим інтерфейсом"""
    print("\n")
    print("ВІТАЄМО У СИСТЕМІ УПРАВЛІННЯ РОЗКЛАДОМ ПОЇЗДІВ!")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nВиберіть опцію (0-5): ").strip()
            
            if choice == '1':
                display_all_trains(trains_schedule)
            elif choice == '2':
                display_sorted_trains(trains_schedule)
            elif choice == '3':
                add_train(trains_schedule)
            elif choice == '4':
                delete_train(trains_schedule)
            elif choice == '5':
                find_trains_at_station(trains_schedule)
            elif choice == '0':
                print("\n")
                print("Дякуємо за використання системи! До побачення!")
                break
            else:
                print("\n❌ Невірний вибір! Будь ласка, виберіть опцію від 0 до 5")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Програма перервана користувачем")
            print("До побачення!\n")
            break
        except Exception as e:
            print(f"\n❌ Непередбачена помилка: {e}")


if __name__ == "__main__":
    main()