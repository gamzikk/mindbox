import math

class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        # Формула Герона для вычисления площади треугольника
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right_angled(self):
        # Проверка, является ли треугольник прямоугольным
        sides = sorted([self.a, self.b, self.c])
        return math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2)

def calculate_area(shape):
    return shape.area()

# Юнит-тесты
def test_circle_area():
    circle = Circle(5)
    assert math.isclose(circle.area(), 78.53981633974483)

def test_triangle_area():
    triangle = Triangle(3, 4, 5)
    assert math.isclose(triangle.area(), 6.0)

def test_right_angled_triangle():
    triangle = Triangle(3, 4, 5)
    assert triangle.is_right_angled()

def test_non_right_angled_triangle():
    triangle = Triangle(3, 4, 6)
    assert not triangle.is_right_angled()

# Пример использования библиотеки
if __name__ == "__main__":
    circle = Circle(5)
    triangle = Triangle(3, 4, 5)

    print("Circle area:", calculate_area(circle))
    print("Triangle area:", calculate_area(triangle))
    print("Is triangle right-angled?", triangle.is_right_angled())

    test_circle_area()
    test_triangle_area()
    test_right_angled_triangle()
    test_non_right_angled_triangle()
    print("All tests passed!")