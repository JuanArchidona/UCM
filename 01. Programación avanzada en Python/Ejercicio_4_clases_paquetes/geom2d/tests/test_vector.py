import pytest
from geom2d.Vector import Vector

@pytest.fixture
def create_vector():
    """
    Crea instancias de vector con los parámetros introducidos
    """
    def _create_vector(x, y):
        return Vector(x, y)
    return _create_vector

@pytest.mark.parametrize("x1, y1, x2, y2, expected", [
    (1.0, 2.0, 1.0, 2.0, True),
    (3.0, 4.0, -3.0, -4.0, False),
])
def test_equality_of_vectors(create_vector, x1, y1, x2, y2, expected):
    v1 = create_vector(x1, y1)
    v2 = create_vector(x2, y2)
    assert (v1 == v2) == expected

@pytest.mark.parametrize("x1, y1, x2, y2, result_x, result_y", [
    (-1.0, -2.0, 3.0, 4.0, 2.0, 2.0),
    (0.0, 0.0, -1.0, -1.0, -1.0, -1.0),
    (5.0, -3.0, -2.0, 3.0, 3.0, 0.0),
])
def test_addition_of_vectors(create_vector, x1, y1, x2, y2, result_x, result_y):
    v1 = create_vector(x1, y1)
    v2 = create_vector(x2, y2)
    result = v1 + v2
    assert result.x == result_x and result.y == result_y