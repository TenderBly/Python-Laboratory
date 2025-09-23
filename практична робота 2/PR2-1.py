import math

def calculate_function(x):
    """
    Функція 1: Обчислює y = sqrt(2) * sin(1/x) + 1
    """
    if x == 0:
        return "Помилка: ділення на нуль!"
    
    y = math.sqrt(2) * math.sin(1/x) + 1
    return y

def is_deficient_number(n):
    """
    Функція 2: Перевіряє, чи є число недостатнім
    Недостатнє число - це натуральне число, сума власних дільників якого менша за саме число
    """
    if n <= 0:
        return False
    
    # Знаходимо всі власні дільники (всі дільники крім самого числа)
    divisors_sum = 0
    for i in range(1, n):
        if n % i == 0:
            divisors_sum += i
    
    return divisors_sum < n

def main():
    print("Програма для обчислення функції та перевірки недостатніх чисел")
    print("=" * 60)
    
    print("\nОберіть опцію:")
    print("1. Обчислити y = √2 * sin(1/x) + 1")
    print("2. Перевірити, чи є число недостатнім")
    
    choice = input("\nВаш вибір (1-2): ")
    
    if choice == '1':
        try:
            x = float(input("Введіть значення x: "))
            result = calculate_function(x)
            if isinstance(result, str):
                print(result)
            else:
                print(f"При x = {x}, y = {result:.6f}")
        except ValueError:
            print("Помилка: введіть числове значення!")
    
    elif choice == '2':
        try:
            n = int(input("Введіть натуральне число: "))
            if is_deficient_number(n):
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