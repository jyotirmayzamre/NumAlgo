class APF:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError('APF must be initialized using a string')
        
        if '.' not in value:
            raise ValueError('APF requires a decimal point for both integers and floats')
        
        
        self.int, self.frac = value.split('.')

        self.int = self.int.lstrip('0') or '0'
        self.frac = self.frac.rstrip('0') or '0'


        
    def __repr__(self):
        return f"{self.int}.{self.frac}"
    

    def __add__(self, num2):
        len1_frac = len(self.frac)
        len2_frac = len(num2.frac)
        max_len_frac = max(len1_frac, len2_frac)

        num1_frac = self.frac.ljust(max_len_frac, '0')
        num2_frac = num2.frac.ljust(max_len_frac, '0')

        num1_frac = num1_frac[::-1]
        num2_frac = num2_frac[::-1]

        result = []
        carry = 0

        for i in range(max_len_frac):
            total = int(num1_frac[i]) + int(num2_frac[i]) + carry
            result.append(str(total % 10))
            carry = total // 10
        

        new_frac = ''.join(reversed(result))
        
        num1_int = self.int[::-1]
        num2_int = num2.int[::-1]
        len1_int = len(num1_int)
        len2_int = len(num2_int)

        result = []
        
        for i in range(max(len1_int, len2_int)):
            x = num1_int[i] if i < len1_int else 0
            y = num2_int[i] if i < len2_int else 0

            total = int(x) + int(y) + carry
            result.append(str(total % 10))
            carry = total // 10
        
        if carry > 0:
            result.append(str(carry))

        new_int = ''.join(reversed(result))

        return APF(f'{new_int}.{new_frac}')

        

    '''
    Calculates self - num2 (assumes num2 <= self)
    '''
    def __sub__(self, num2):
        len1_frac = len(self.frac)
        len2_frac = len(num2.frac)
        max_len_frac = max(len1_frac, len2_frac)

        num1_frac = self.frac.ljust(max_len_frac, '0')
        num2_frac = num2.frac.ljust(max_len_frac, '0')

        num1_frac = num1_frac[::-1]
        num2_frac = num2_frac[::-1]

        result = []
        borrow = 0


        for i in range(max_len_frac):
            x = int(num1_frac[i]) - borrow
            y = int(num2_frac[i])

            if x < y:
                x += 10
                borrow = 1
            else:
                borrow = 0

            result.append(str(x-y))

        new_frac = ''.join(reversed(result))
        
        result = []
        num1_int = self.int[::-1]
        num2_int = num2.int[::-1]

        len1_int = len(num1_int)
        len2_int = len(num2_int)

        for j in range(max(len1_int, len2_int)):
            x = int(num1_int[j]) - borrow
            y = int(num2_int[j]) if j < len2_int else 0

            if x < y:
                x += 10
                borrow = 1
            else:
                borrow = 0

            result.append(str(x-y))
        
        new_int = ''.join(reversed(result))

        return APF(f'{new_int}.{new_frac}')

        
    def __mul__(self, num2):
        #convert both to integers

        normal1 = self.int + self.frac
        normal1 = normal1.strip('0') or '0'
        normal1 = normal1[::-1]
        normal1_frac_len = len(self.frac)
       

        normal2 = num2.int + num2.frac
        normal2 = normal2.strip('0') or '0'
        normal2 = normal2[::-1]
        normal2_frac_len = len(num2.frac)

        result = [0] * (len(normal1) + len(normal2))

        for i in range(len(normal1)):
            carry = 0
            for j in range(len(normal2)):
                total = result[i+j] + int(normal1[i]) * int(normal2[j]) + carry
                result[i+j] = total % 10
                carry = total // 10
            if carry:
                result[i + len(normal2)] += carry


        new_frac = []
        new_int = []
        for i in range(len(normal1) + len(normal2)):
            if i >= normal1_frac_len + normal2_frac_len:
                new_int.append(str(result[i]))
            else:
                new_frac.append(str(result[i]))
        
        return APF(f'{"".join(reversed(new_int))}.{"".join(reversed(new_frac))}')


class CN:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __repr__(self):
        return f"{self.real} + {self.imag}i"
        
    def __add__(self, num):
        if isinstance(num, CN):
            return CN(self.real + num.real, self.imag + num.imag)
        
        else:
            raise TypeError('Second operand is not the correct type')
        
    def __mul__(self, num):
        if isinstance(num, CN):
            return CN(self.real * num.real - self.imag * num.imag, self.real * num.imag + self.imag * num.real)
        else:
            raise TypeError('Second operand is not the correct type')
        
    def __truediv__(self, num):
        if isinstance(num, CN):
            denom = num.real * num.real + num.imag * num.imag
            if denom == 0:
                raise ZeroDivisionError('Division by 0 not allowed')
            else:
                real = (self.real * num.real + self.imag * num.imag) / denom
                imag = (self.imag * num.real - self.real * num.imag) / denom
                return CN(real, imag)
            
        else:
            raise TypeError('Second operand is not the correct type')

    def __abs__(self):
        sum = self.real * self.real + self.imag * self.imag
        return sum**0.5
    
    def cc(self):
        return CN(self.real, -self.imag)


class vec:
    def __init__(self, field: str, length: int, val: list):
        if field not in ('real', 'complex'):
            raise ValueError('Field has to be either "real" or "complex"')
        
        if length != len(val):
            raise ValueError('Input length and length of values dont match')
        
        expected_type = float if field == 'real' else CN

        for i in val:
            if not isinstance(i, expected_type):
                raise ValueError('Vector value inputs are not consistent in type')
            
        self.field = field
        self.length = length
        self.val = val

    def __repr__(self):
        return str(self.val)
    
    def __add__(self, vec2):
        if(self.field != vec2.field):
            raise TypeError('Mismatch between fields of vectors')
        
        if self.length != vec2.length:
            raise ValueError('Vectors have different dimensions')
        
        return vec(self.field, self.length, [self.val[i] + vec2[i] for i in range(self.length)])
    
    #dot product
    def __mul__(self, vec2):
        if(self.field != vec2.field):
            raise TypeError('Mismatch between fields of vectors')
        
        if self.length != vec2.length:
            raise ValueError('Vectors have different dimensions')
        
        sum = 0
        for i in range(self.length):
            sum += self.val[i] * vec2.val[i]
        
        return sum


class mat:
    def __init__(self, field, n, m, cols):
        if field not in ('real', 'complex'):
            raise ValueError('Field has to be either "real" or "complex"')
        
        if len(cols) != m:
            raise ValueError('Dimension error: number of input columns doesnt match m')
        
        expected_type = float if field == 'real' else CN 
        for i in cols:
            if i.length != n:
                raise ValueError('Dimension error: length of input columns doesnt match n')
            
            for j in i.val:
                if not isinstance(j, expected_type):
                    raise ValueError('Type error: columns are not consistent in type')

        self.field = field
        self.n = n
        self.m = m
        self.cols = cols

    def __repr__(self):
        return f"{self.cols}"

        
    def __add__(self, m2):
        if self.field != m2.field:
            raise TypeError('Mismatch between fields')
        
        if self.n != m2.n or self.m != m2.m:
            raise ValueError('Mismatch between dimensions')
        
        new_cols = []

        for i in range(self.m):
            new_cols.append(self.cols[i] + m2.cols[i])
        
        return mat(self.field, self.n, self.m, new_cols)
    
    
    def __mul__(self, m2):
        if self.field != m2.field:
            raise TypeError('Mismatch between fields')
        
        if self.m != m2.n:
            raise ValueError('Mismatch between dimensions')
        
        result = []
        for j in range(m2.m):
            current_col = m2.cols[j]
            new_col = []
            for i in range(self.n):
                row = vec(self.field, self.m, [col.val[i] for col in self.cols])
                new_col.append(row*current_col)
            result.append(vec(self.field, self.n, new_col))
        return mat(self.field, self.n, m2.m, result)
    
    def get_row(self, row):
        if(row < 1 or row > self.n):
            raise ValueError('Row is out of bounds')
        
        if(self.field == 'real'):
            basis = mat('real', 1, self.n, [vec('real', 1, [1.0 if j == (row - 1) else 0.0]) for j in range(self.n)])

        else:
            basis = mat('complex', 1, self.n, [vec('real', 1, [CN(1.0, 0) if j == (row - 1) else CN(0.0, 0.0)]) for j in range(self.n)])

        return basis * self
    
    def get_col(self, col):
        if(col < 1 or col > self.m):
            raise ValueError('Column is out of bounds')
        
        if(self.field == 'real'):
            basis = mat('real', self.m, 1, [vec('real', self.m, [1.0 if i == col - 1 else 0.0 for i in range(self.m)])])

        else:
            basis = mat('real', self.m, 1, [vec('real', self.m, [CN(1.0, 0.0) if i == col - 1 else CN(0.0, 0.0) for i in range(self.m)])])
      
        return  self*basis
    
    def transpose(self):
        new_cols = []
        for i in range(self.n):
            nCol = [self.cols[j].val[i] for j in range(self.m)]
            new_cols.append(vec(self.field, self.m, nCol))
        
        return mat(self.field, self.m, self.n, new_cols)
    
    def conj(self):
        if(self.field == 'real'):
            return self
        else:
            new_cols = []
            for col in self.cols:
                conj_vals = [val.cc() for val in col.val]
                new_cols.append(vec('complex', col.length, conj_vals))
            
            return mat('complex', self.n, self.m, new_cols)
        
    def conj_transpose(self):
        transpose = self.transpose()
        return transpose.conj()



class Poly:

    #Assuming trailing zeros are not included in the coeffs (leading zeros are okay)
    def __init__(self, coeffs: list, field: str):
        if not isinstance(coeffs, list):
            raise TypeError("Input is not a list of coefficients")
        
        if(len(coeffs) == 0):
            raise ValueError("Input must have at least one element")

        if field not in ("real", "complex"):
            raise ValueError("Field must be either real or complex")
        
        self.coeffs = coeffs  
        self.field = field

    def __repr__(self) -> str:
        terms = []
        for i, c in enumerate(self.coeffs):
            if self.field == 'real':
                val = c
            else:
                val = f"({c.real} + {c.imag}i)"

            if c != 0:
                if i == 0:
                    terms.append(f"{val}")
                elif i == 1:
                    terms.append(f"{val}x")
                else:
                    terms.append(f"{val}x^{i}")
        return " + ".join(terms) if terms else "0"
    

    def __add__(self, poly):
        if not isinstance(poly, Poly):
            raise TypeError("Second polynomial is not the correct type")
        
        if self.field != poly.field:
            raise TypeError("Polynomials have a field mismatch")
        
        if self.field == 'real':
            default = 0.0
        else:
            default = CN(0.0, 0.0)
        
        terms = []
        len1 = len(self.coeffs)
        len2 = len(poly.coeffs)
        for i in range(max(len1, len2)):
            a = self.coeffs[i] if i < len1 else default
            b = poly.coeffs[i] if i < len2 else default

            #ignore this error, it is there because of type ambiguity in python
            terms.append(a+b)

        return Poly(terms, self.field)
    
    def __mul__(self, poly):
        if not isinstance(poly, Poly):
            raise TypeError("Second polynomial is not the correct type")
        
        if self.field != poly.field:
            raise TypeError("Polynomials have a field mismatch")
        
        len1, len2 = len(self.coeffs), len(poly.coeffs)

        result = [0.0 if self.field == 'real' else CN(0.0, 0.0) for i in range(len1+len2-1)]

        for i in range(len1):
            for j in range(len2):
                result[i+j] += self.coeffs[i] * poly.coeffs[j]
        
        return Poly(result, self.field)


    def eval(self, x):

        if self.field == 'real' and isinstance(x, CN):
            raise TypeError('Cannot evaluate a real polynomial at a complex point')
        
        if self.field == 'complex' and isinstance(x, float | int):
            raise TypeError('Cannot evaluate a complex polynomial at a real point')

        if self.field == 'real':
            result = 0.0
            term = 1.0
        else:
            result = CN(0, 0)
            term = CN(1, 0)

        for i in range(len(self.coeffs)):
            result += self.coeffs[i] * term
            term *= x

        return result
    
    def degree(self):
        return len(self.coeffs) - 1

    def derivative(self):
        terms = []
        for i in range(1, len(self.coeffs)):
            terms.append(self.coeffs[i] * (i if self.field == 'real' else CN(i, 0)))
        return Poly(terms, self.field)
    


