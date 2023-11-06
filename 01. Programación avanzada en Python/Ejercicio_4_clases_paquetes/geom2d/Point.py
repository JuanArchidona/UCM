from geom2d.Vector import Vector
from typing import Self
import math


class Point:
    """
    Representa un punto en un espacio bidimensional.
    """

    def __init__(self, x: float, y: float):
        """
        Inicializa un nuevo punto en las coordenadas x e y.
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        Obtiene la coordenada X del punto.
        """
        return self._x

    @property
    def y(self):
        """
        Obtiene la coordenada Y del punto.
        """
        return self._y

    @x.setter
    def x(self, new_x):
        """
        Establece un nuevo valor para la coordenada X del punto.
        """
        self._x = new_x

    @y.setter
    def y(self, new_y):
        """
        Establece un nuevo valor para la coordenada Y del punto.
        """
        self._y = new_y

    def __hash__(self):
        """
        Genera un valor hash único para este punto.
        """
        return hash((self._x, self._y))

    def __eq__(self, other: Self) -> bool:
        """
        Compara este punto con otro para verificar si son iguales.
        """
        return self._x == other.x and self._y == other.y

    def __sub__(self, other: Self) -> Vector:
        """
        Define la resta de dos puntos, resultando en un vector.
        """
        if not isinstance(other, Point):
            raise TypeError("La resta solo se puede ejecutar con otro objeto de tipo Point")
        return Vector(self._x - other.x, self._y - other.y)

    def distance(self, other: Self) -> float:
        """
        Calcula la distancia euclidiana hasta otro punto.
        """
        if isinstance(other, Point):
            return math.sqrt((self._x - other.x) ** 2 + (self._y - other.y) ** 2)
        else:
            raise ValueError("El parámetro debe ser una instancia de la clase Point")

    def __str__(self):
        """
        Representación informal del punto como cadena de texto.
        """
        return f"Objeto de la clase Point con parámetros (x={self._x}, y={self._y})"

    def __repr__(self):
        """
        Representación formal del punto.
        """
        return f"Point(x={self._x}, y={self._y})"
