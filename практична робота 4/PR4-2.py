n = 7

a = [[(0 if j < min(i+1, n-i) else 1) for j in range(n)] for i in range(n)]

for r in a:
    print(*r)
