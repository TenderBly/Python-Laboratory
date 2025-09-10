print("Введіть значення a і b:")
a = int(input ("Введіть а: "))
while a < 1 or a > 100:
    a = int(input ("Введіть ще раз а: "))
b = int(input ("Введіть b: "))
while b < 1 or b > 100:
    b = int(input ("Введіть ще раз b: "))
    
if a > b:  
    x = b * a + 1  
    print("Значення X =", x)
elif a == b:  
    x = 3425  
    print("Значення X =", x)
else:  
    x = (2 * a - 5) / b  
    print("Значення X =", x)  