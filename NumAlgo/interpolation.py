from classes import Poly

def Lagrange_interpolation(points: list[tuple[float, float]]) -> Poly:
    polynomial = Poly([0.0], 'real')

    length = len(points)

    for i in range(length):
        num = Poly([1.0], 'real')
        denom = 1.0
        for j in range(length):
            if i == j:
                continue

            num *= Poly([-points[j][0], 1.0], 'real')
            denom *= (points[i][0] - points[j][0])

        mid = num * Poly([1 / denom], 'real')
        polynomial += mid * Poly([points[i][1]], 'real')
    
    return polynomial


def Divided_difference(points: list[tuple[float, float]]) -> float:
    length = len(points)
    if(length == 1):
        return points[0][1]
    
    
    num = Divided_difference(points[1:]) - Divided_difference(points[:-1])
    denom = points[length-1][0] - points[0][0]

    return num / denom

def Divided_difference_table(points: list[tuple[float, float]]) -> list[list[float]]:
    length = len(points)

    table = [[0.0]*length for i in range(length)]

    for i in range(length):
        table[i][0] = points[i][1]

    for k in range(1, length):
        for i in range(length-k):
            table[i][k] = (table[i+1][k-1] - table[i][k-1]) / (points[i+k][0] - points[i][0])
    
    return table

def Newton_interpolation(points: list[tuple[float, float]]) -> Poly:
    length = len(points)
    table = Divided_difference_table(points)

    polynomial = Poly([table[0][0]], 'real')
    prod = Poly([1.0], 'real')

    for i in range(1, length):
        prod *= Poly([-points[i-1][0], 1.0], 'real')
        polynomial += Poly([table[0][i]], 'real') * prod

    return polynomial



def Hermite_interpolation(points: list[tuple[float, float, float]]) -> Poly:
    polynomial = Poly([0.0], 'real')

    for i in range(len(points)):
        num = Poly([1.0], 'real')
        denom = 1.0

        for j in range(len(points)):
            if i == j:
                continue

            num *= Poly([-points[j][0], 1.0], 'real')
            denom *= (points[i][0] - points[j][0])
        
        basis = num * Poly([1 / denom], 'real')



        term = basis * basis
        derivative = Poly([basis.derivative().eval(points[i][0])], 'real')
        expr = Poly([-points[i][0], 1.0], 'real')

        h_i_x = term * (derivative * expr * Poly([-2.0], 'real') + Poly([1.0], 'real'))
        k_i_x = term * expr
        polynomial += (Poly([points[i][1]], 'real') * h_i_x) + (Poly([points[i][2]], 'real') * k_i_x)


    return polynomial

