import math
from typing import Self


class Vector:
    """
    Representa un vector en un espacio bidimensional.
    """

    def __init__(self, x: float, y: float):
        """
        Inicializa un nuevo vector con las componentes x e y.
        """
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        """
        Obtiene la componente X del vector.
        """
        return self._x

    @property
    def y(self) -> float:
        """
        Obtiene la componente Y del vector.
        """
        return self._y

    @property
    def mod(self) -> float:
        """
        Calcula el módulo (longitud) del vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other: Self) -> bool:
        """
        Compara este vector con otro para verificar si son iguales.
        """
        return self.x == other.x and self.y == other.y

    def __le__(self, other: Self) -> bool:
        """
        Verifica si este vector es menor o igual en módulo que otro vector.
        """
        return self.mod <= other.mod

    def __hash__(self):
        """
        Genera un valor hash único para este vector.
        """
        return hash((self._x, self._y, "vector"))

    def __add__(self, other: Self) -> Self:
        """
        Define la suma de este vector con otro.
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        """
        Define la resta de este valor con otro,
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Self:
        """
        Define el vector opuesto (negativo) de este vector.
        """
        return Vector(-self.x, -self.y)

    def __mul__(self, other: Self) -> float:
        """
        Define el producto escalar de este vector con otro.
        """
        return self.x * other.x + self.y * other.y

    def __rmul__(self, scalar: float) -> 'Vector':
        """
        Define la multiplicación de este vector por un escalar.
        """
        return Vector(scalar * self.x, scalar * self.y)

    def __repr__(self) -> str:
        """
        Representación formal del vector.
        """
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        """
        Representación informal del vector como cadena de texto.
        """
        return f"({self.x:.4f}, {self.y:.4f})"
