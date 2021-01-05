class Matrix:
    def __init__(self, n, m, matrix):
        self.n = n
        self.m = m
        self.matrix = matrix

    def __add__(self, other):
        if isinstance(other, self.__class__):
            if self.n != other.n or self.m != other.m:
                print("ERROR")
            else:
                C = [[number(self.matrix[i][j]) + number(other.matrix[i][j]) for j in range(self.m)]
                     for i in range(self.n)]
                return Matrix(self.n, self.m, C)
        elif isinstance(other, (int, float)):
            C = [[other + number(self.matrix[i][j]) for j in range(self.m)] for i in range(self.n)]
            return Matrix(self.n, self.m, C)
        else:
            print(f"Unsupported operand {other}")

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            if self.m != other.n:
                print("ERROR")
            else:
                C = [[sum([number(self.matrix[i][k]) * number(other.matrix[k][j])
                           for k in range(self.m)])
                      for j in range(other.m)]
                     for i in range(self.n)]
                return Matrix(self.n, other.m, C)
        elif isinstance(other, (int, float)):
            C = [[other * number(self.matrix[i][j]) for j in range(self.m)] for i in range(self.n)]
            return Matrix(self.n, self.m, C)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self * other

    def transpose(self, transposition='main'):
        transposed = self.matrix.copy()
        if transposition == 'main':  # normal transposition
            pass
        elif transposition == 'side':  # side diagonal transposition
            transposed = [line[::-1] for line in reversed(transposed)]
        elif transposition == 'vertical':  # vertical transposition
            C = [line[::-1] for line in transposed]
            return Matrix(self.n, self.m, C)
        elif transposition == 'horizontal':  # horizontal transposition
            C = [line for line in reversed(transposed)]
            return Matrix(self.n, self.m, C)
        else:
            print("Unknown type of transposition")
            return None
        C = [[number(transposed[j][i]) for j in range(self.n)] for i in range(self.m)]
        return Matrix(self.n, self.m, C)

    def __cofactor(self, minor, size, n, m):
        new_minor = [[number(minor[i][j]) for j in range(size) if j != m]
                     for i in range(size) if i != n]
        cofactor = pow(-1, n + m) * self.determinant(new_minor, size - 1)
        return cofactor

    def determinant(self, minor=None, size=None):
        minor = self.matrix if minor is None else minor
        size = len(minor) if size is None else size
        if size == 1:
            return number(minor[0][0])
        if size == 2:
            return number(minor[0][0]) * number(minor[1][1]) - \
                   number(minor[0][1]) * number(minor[1][0])
        else:
            n = 0
            det = 0
            for m in range(size):
                cofactor = self.__cofactor(minor, size, n, m)
                det += number(minor[n][m]) * cofactor
        return det

    def inverse(self):
        det_matrix = self.determinant(self.matrix, self.n)
        if det_matrix == 0:
            print("This matrix doesn't have an inverse.")
            return None
        else:
            cofactors = [[self.__cofactor(self.matrix, self.n, n, m)
                          for m in range(self.n)]
                         for n in range(self.n)]
            adj_matrix = Matrix(self.n, self.n, cofactors).transpose()
            inverse = (1 / det_matrix) * adj_matrix
            return inverse

    def print(self):
        print()
        for i in self.matrix:
            print(*i)
        print()


# Constants
MAIN_MENU = "\n1. Add matrices\n" \
            "2. Multiply matrix by a constant\n" \
            "3. Multiply matrices\n" \
            "4. Transpose matrix\n" \
            "5. Calculate a determinant\n" \
            "6. Inverse matrix\n" \
            "0. Exit"

TRANSPOSE_MENU = "\n1. Main diagonal\n" \
                 "2. Side diagonal\n" \
                 "3. Vertical line\n" \
                 "4. Horizontal line\n"

TRANSPOSITIONS = {'1': 'main',
                  '2': 'side',
                  '3': 'vertical',
                  '4': 'horizontal'}


# helper functions
def number(str_x):
    """Converts str_x to int or float"""
    try:
        # multiplied and divided by 100 to overcome rounding bug
        x = round((float(str_x) * 100) / 100, 4)
        return int(x) if x.is_integer() else x
    except ValueError:
        print(f"{str_x} is not a number")


def read_matrix(size_msg="Enter size of matrix: ", matrix_msg="Enter matrix: "):
    print(size_msg)
    n, m = map(int, input().split())
    print(matrix_msg)
    matrix = [input().split() for _ in range(n)]
    return n, m, matrix


def print_error(message="The operation cannot be performed."):
    print(message)


def menu():
    print(MAIN_MENU)
    inp = input("Your choice: ")
    if inp == '1':
        A = Matrix(*read_matrix("Enter size of first matrix: ",
                                "Enter first matrix: "))
        B = Matrix(*read_matrix("Enter size of second matrix: ",
                                "Enter second matrix: "))
        C = A + B
        C.print()
    elif inp == '2':
        A = Matrix(*read_matrix())
        print("Enter constant: ")
        k = number(input())
        C = k * A
        C.print()
    elif inp == '3':
        A = Matrix(*read_matrix("Enter size of first matrix: ",
                                "Enter first matrix: "))
        B = Matrix(*read_matrix("Enter size of second matrix: ",
                                "Enter second matrix: "))
        C = A * B
        C.print()
    elif inp == '4':
        print(TRANSPOSE_MENU)
        choice = input("Your choice: ")
        A = Matrix(*read_matrix())
        try:
            A.transpose(TRANSPOSITIONS[choice]).print()
        except KeyError:
            print("Wrong choice of transposition type!")
    elif inp == '5':
        A = Matrix(*read_matrix())
        print("The result is")
        detA = A.determinant()
        print(detA)
    elif inp == '6':
        A = Matrix(*read_matrix())
        print("The result is", end='')
        A.inverse().print()
    elif inp == '0':
        return False
    else:
        print_error()
    menu()

repeat = True
while repeat:
    repeat = menu()