class X:
    def __init__(self):
        pass

    def __repr__(self):
        return "X"

    def evaluate(self, x_value):
        # X evaluates to the provided x_value wrapped in Int
        return Int(x_value)

    def simplify(self):
        # X cannot be simplified further
        return self


class Int:
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return str(self.i)

    def evaluate(self, x_value):
        # Constant evaluates to itself
        return Int(self.i)

    def simplify(self):
        # Integer constants are already simplest
        return self


class Add:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return repr(self.p1) + " + " + repr(self.p2)

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        return Int(v1.i + v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simplify()

        # 0 + X -> X, X + 0 -> X
        if isinstance(s1, Int) and s1.i == 0:
            return s2
        if isinstance(s2, Int) and s2.i == 0:
            return s1

        # 3 + 5 -> 8
        if isinstance(s1, Int) and isinstance(s2, Int):
            return Int(s1.i + s2.i)

        return Add(s1, s2)


class Mul:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        if isinstance(self.p1, Add):
            if isinstance(self.p2, Add):
                return "( " + repr(self.p1) + " ) * ( " + repr(self.p2) + " )"
            return "( " + repr(self.p1) + " ) * " + repr(self.p2)
        if isinstance(self.p2, Add):
            return repr(self.p1) + " * ( " + repr(self.p2) + " )"
        return repr(self.p1) + " * " + repr(self.p2)

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        return Int(v1.i * v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simplify()

        # X * 0 -> 0, 0 * X -> 0
        if (isinstance(s1, Int) and s1.i == 0) or (isinstance(s2, Int) and s2.i == 0):
            return Int(0)

        # X * 1 -> X, 1 * X -> X
        if isinstance(s1, Int) and s1.i == 1:
            return s2
        if isinstance(s2, Int) and s2.i == 1:
            return s1

        # 3 * 5 -> 15
        if isinstance(s1, Int) and isinstance(s2, Int):
            return Int(s1.i * s2.i)

        return Mul(s1, s2)


class Sub:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        # Parenthesize additive expressions to avoid ambiguity:
        # (a + b) - c, a - (b + c), also for nested Sub on the right
        left = repr(self.p1) if not isinstance(self.p1, (Add, Sub)) else "( " + repr(self.p1) + " )"
        right = repr(self.p2) if not isinstance(self.p2, (Add, Sub)) else "( " + repr(self.p2) + " )"
        return f"{left} - {right}"

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        return Int(v1.i - v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simplify()

        # X - 0 -> X
        if isinstance(s2, Int) and s2.i == 0:
            return s1

        # 5 - 3 -> 2
        if isinstance(s1, Int) and isinstance(s2, Int):
            return Int(s1.i - s2.i)

        return Sub(s1, s2)


class Div:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        # Parenthesize additive/subtractive expressions to avoid ambiguity
        left = repr(self.p1) if not isinstance(self.p1, (Add, Sub)) else "( " + repr(self.p1) + " )"
        right = repr(self.p2) if not isinstance(self.p2, (Add, Sub)) else "( " + repr(self.p2) + " )"
        return f"{left} / {right}"

    def evaluate(self, x_value):
        v1 = self.p1.evaluate(x_value)
        v2 = self.p2.evaluate(x_value)
        # Use integer division; let ZeroDivisionError propagate if v2.i == 0
        return Int(v1.i // v2.i)

    def simplify(self):
        s1 = self.p1.simplify()
        s2 = self.p2.simpli
