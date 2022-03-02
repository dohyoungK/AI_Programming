'''201624419/KimDoHyoung'''

coefficient = input("Enter coefficient of restitution: ")
coefficient = float('0' + coefficient)
height = float(input("Enter initial height in meter: "))

bounce = 1
result = height
height *= coefficient

while height >= 0.1:
    result += height * 2
    height *= coefficient
    bounce += 1

print("Number of bounces:", bounce)
print("Meters traveled:", round(result,2))

