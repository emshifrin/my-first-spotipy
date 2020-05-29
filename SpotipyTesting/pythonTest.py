print("Hello World")


## count the numbers from 1 to x

def sumAllFrom1(x):
    if (x == 0):
        return 0
    elif (x == 1):
        return 1
    else:
        return x + sumAllFrom1(x - 1)

print(sumAllFrom1(7))

