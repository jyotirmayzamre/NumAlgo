def machine_epsilon() -> float:
    epsilon = 1.0
    while 1.0 + epsilon / 2.0 != 1.0:
        epsilon /= 2.0
    return epsilon

def check_limits():
    #Overflow

    x = 1.0
    while True:
        prev = x
        x *= 2
        if x == float('inf'):
            break
    print("Approx Overflow limit: ", prev)

    y = 1.0
    while True:
        prev = y
        y /= 2
        if y == 0.0:
            break
    print("Approx Underflow limit: ", prev)


def convert_base(base_input: int, base_output: int, num: list[int]) -> list[int]:

    if not isinstance(base_input, int) or not isinstance(base_output, int) or not isinstance(num, list):
        raise TypeError("Input types are incorrect")

    decimal = 0
    for i in range(len(num)):
        decimal += num[i] * (base_input**i)
    
    result = []
    if decimal == 0:
        return [0]
    
    while decimal > 0:
        result.append(int(decimal % base_output))
        decimal  = decimal // base_output
    return result


def madhava_series(iter: int) -> float:
    denominator = 1.0
    numerator = 1.0
    result = 0

    for i in range(1, iter+1):
        result += numerator / denominator
        denominator += 2.0
        numerator = - numerator
    return result * 4

def nilkantha_series(iter: int) -> float:
    result = 3.0
    numerator = 4.0
    denom_1 = 2.0
    denom_2 = 3.0
    denom_3 = 4.0

    for i in range(1, iter + 1):
        result += numerator / (denom_1 * denom_2 * denom_3)
        denom_1 += 2.0
        denom_2 += 2.0
        denom_3 += 2.0
        numerator = -numerator

    return result


def euler_formula(iter: int) -> float:
    result = 1.0

    for i in range(1,iter):
        num_result = 1.0
        num_term = 1.0
        denom_result = 1.0
        denom_term = 3.0

        for j in range(1, i+1):
            num_result *= num_term
            denom_result *= denom_term
            num_term += 1.0
            denom_term += 2.0
        
        result += (num_result / denom_result)
    return result * 2.0


def newton_formula(iter: int) -> float:
    result = (3 * (3**0.5)) / 4
    
    num = 1.0
    denom_1 = 4.0
    denom_2 = 1.0
    denom_3 = -1.0
    denom_4 = 3.0
    term = 0.0

    for i in range(iter-1):
        term += num / (denom_1 * (denom_2**2) * denom_3 * denom_4)
        num *= (2*i + 1) * (2*i + 2)
        denom_1 *= 16.0
        denom_2 *= i+1
        denom_3 += 2.0
        denom_4 += 2.0

    result += -24.0 * term
    return result



def ramanujan_formula(iter: int) -> float:
    factor = (2 * (2**0.5)) / 9801

    result = 0
    k_factorial = 1.0
    four_k_factorial = 1.0

    for i in range(iter):
        num = four_k_factorial * (1103 + 26390 * i)
        denom = k_factorial**4 * (396 ** (4*i))
        result += num / denom

        k_factorial *= (i+1)
        four_k_factorial *= (4*i + 4) * (4*i + 3) * (4*i + 2) * (4*i + 1)

    final = 1 / (factor * result)
    return final


def e_x(iter: int, input: float) -> float:
    result = 0.0
    term = 1.0

    for i in range(iter):
        result += term
        term *= input / (i+1)

    return result


def sin_x(iter: int, input: float) -> float:
    result = 0.0
    term  = input

    for i in range(iter):
        result += term
        term *= ((-input*input)) / ((2*i + 2) * (2*i + 3))
        

    return result



def cos_x(iter: int, input: float) -> float:
    result = 0.0
    term = 1.0

    for i in range(iter):
        result += term
        term *= (-input*input) / ((2*i+1) * (2*i+2))

    return result


def log_one_plus_x(iter: int, input: float) -> float:
    if input < -1.0 or input > 1.0:
        raise TypeError('Absolute value of input should be less than 1')

    term = input
    result = 0.0

    for i in range(1, iter + 1):
        result += term / i
        term *= -input
    
    return result
        

def one_upon_one_minus_x(iter: int, input: float) -> float:
    if input < -1.0 or input > 1.0:
        raise TypeError('Absolute value of input should be less than 1')
    
    result = 0.0
    term = 1.0
    for i in range(iter):
        result += term
        term *= input

    return result


def compute_e() -> float:
    eps = machine_epsilon()
    
    result = 1.0
    fact = 1.0
    prev = 0.0
    i = 1
    while (result - prev) > eps:
        prev = result
        result += 1 / fact
        i += 1
        fact *= i

    return result


def ln_x(x: float, max_iter=100) -> float:
    if x <= 0:
        raise ValueError('X should be greater than 0')

    e = compute_e()
    epsilon = machine_epsilon()

    y = x - 1.0
    for i in range(max_iter):
        y_new = y + x / e**y - 1
        if abs(y_new - y) < epsilon:
            return y_new
        y = y_new

    return y

     