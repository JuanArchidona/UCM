from geom2d.Point import Point
from geom2d.Vector import Vector
import pytest
import math

@pytest.fixture
def mock_point_1() -> Point:
    return Point(1, 1)

@pytest.fixture
def mock_point_2() -> Point:
    return Point(4, 5)

def test_getter(mock_point_1):
    assert mock_point_1.x == 1 and mock_point_1.y == 1

def test_setter(mock_point_1):
    mock_point_1.x = 10
    mock_point_1.y = 10
    assert mock_point_1.x == 10 and mock_point_1.y == 10

def test_sub(mock_point_1, mock_point_2):
    """
    Es el resultado esperado del vector que va desde mock_point_2 a mock_point_1
    """
    result = mock_point_1 - mock_point_2
    assert result.x == pytest.approx(-3, abs=1e-4)
    assert result.y == pytest.approx(-4, abs=1e-4)

    with pytest.raises(TypeError):
        mock_point_1 - 123

def test_distance(mock_point_1, mock_point_2):
    """
    Calcula la diferencia esperada usando la fórmula de la distancia entre dos puntos
    """
    result = mock_point_1.distance(mock_point_2)
    expected_distance = math.sqrt((4 -1) ** 2 + (5 - 1) ** 2)
    assert result == pytest.approx(expected_distance, abs= 1e-4)

    with pytest.raises(ValueError):
        mock_point_1.distance("string")