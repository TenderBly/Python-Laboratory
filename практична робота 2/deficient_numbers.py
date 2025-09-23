def is_deficient_number(n):
    """
    Перевіряє, чи є число недостатнім.
    Недостатнє число - це натуральне число, сума власних дільників якого менша за саме число.
    """
    if n <= 0:
        return False
    
    # Знаходимо всі власні дільники (всі дільники крім самого числа)
    divisors_sum = 0
    for i in range(1, n):
        if n % i == 0:
            divisors_sum += i
    
    return divisors_sum < n