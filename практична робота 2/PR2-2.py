import math
import deficient_numbers

def main():
    print("Програма для обчислення функції та перевірки недостатніх чисел")
    print("=" * 60)
    
    print("\nОберіть опцію:")
    print("1. Перевірити, чи є число недостатнім")
    
    choice = input("\nВаш вибір?: ")

    if choice == '1':
        try:
            n = int(input("Введіть натуральне число: "))
            if deficient_numbers.is_deficient_number(n):
                print(f"Число {n} є недостатнім")
            else:
                print(f"Число {n} не є недостатнім")
        except ValueError:
            print("Помилка: введіть ціле число!")
    
    else:
        print("Неправильний вибір.")
    
    print("\nПрограма завершена.")

if __name__ == "__main__":
    main()