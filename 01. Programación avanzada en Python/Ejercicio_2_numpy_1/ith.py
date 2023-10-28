# imports

import numpy as np


def summary(a: np.ndarray) -> tuple[float, float, float, float]:
    """
    function that returns the minimum, maximum, mean and standard deviation of an array
    :param a: ndarray
    :return: tuple of float
       a tuple of four float values: min, max, mean, std
    Examples
    --------
    >>> summary(np.array([[1,2,3], [4,5,6]]))   # array sin nan
    (1, 6, 3.5, 1.707825127659933)
    >>> summary(np.array([[1,np.nan,3], [4,5,6]]))   # array con un nan
    (nan, nan, nan, nan)
    >>> summary(np.array([]))   # array vacío
    Traceback (most recent call last):
    ...
    ValueError: zero-size array to reduction operation minimum which has no identity
    """

    if a.size == 0:
        raise ValueError("El array está vacío")

    return np.nanmin(a), np.nanmax(a), np.nanmean(a), np.nanstd(a)

def check_nulls(a: np.ndarray) -> bool:
    """
    function that checks the validity od sensor data
    :param a: np.ndarray
    :return: bool
       indicates if data contains nan
    Examples
    --------
    >>> check_nulls(np.array([[1,2,3], [4,5,6]]))   # array sin nan
    True
    >>> check_nulls(np.array([[1,np.nan,3], [4,5,6]]))   # array con un nan
    False
    >>> check_nulls(np.array([]))   # array vacío
    True
    """
    return not np.isnan(a).any()


def ith(temperature: np.ndarray, humidity: np.ndarray) -> np.ndarray:
    """
    Calculates the temperature-humidity index (THI) of each of the grid cells.
    The ith-value of each cell must be rounded to the nearest integer
    :param temperature:  np.ndarray
        temperatures collected by the sensor in a grid
    :param humidity:  np.ndarray
        humidity data collected by the sensor on a grid
    :return:  np.ndarray
        temperature-humidity index (THI) (round to the nearest integer)
    :raise ValueError: if shape of input arrays is not the same
    >>> ith(np.array([[1,2,3], [4,5,6]]), np.array([[1,2,3], [4,5,6]]))
    array([[47., 48., 48.],
           [49., 50., 51.]])
    >>> ith(np.array([[1,np.nan,3], [4,5,6]]), np.array([[1,2,3], [4,5,6]]))
    array([[47., nan, 48.],
           [49., 50., 51.]])
    >>> ith(np.array([[1], [4]]), np.array([[1], [4]]))
    array([[47.],
           [49.]])
    >>> ith(np.array([[2,3], [4,5]]), np.array([[1,2,3], [4,5,6]]))  # dimensiones distintas
    Traceback (most recent call last):
        ...
    ValueError: Shape of data sensors must be the same. Temperature: (2, 2) != humidity: (2, 3)
    """
    if temperature.shape != humidity.shape:
        raise ValueError(f"El tamaño de los datos de los dos sensores debe ser igual: {temperature.shape}")

    ith_array = 0.8 + temperature + (humidity/100) * (temperature - 14.3) + 46.4

    return np.around((ith_array))


def isStress(ith: np.ndarray) -> np.ndarray:
    """
    Determines the grid points where serious stress occurs.
    :param ith: np.ndarray
       temperature-humidity index (THI)
    :return: np.ndarray
       True values indicate ser<zsdaious stress
    >>> isStress(np.array([[47.], [49.]]))
    array([[False],
           [False]])
    >>> isStress(np.array([[47., 79., 48.], [49.,50. ,81.]]))
    array([[False,  True, False],
           [False, False,  True]])
    >>> isStress(np.array([[80, np.nan, 48.], [49., 50., 88.]]))
    array([[ True, False, False],
           [False, False,  True]])
    """
    return ith > 78


# ------------ test  ----------------#
import doctest

def test_doc() -> None:
    """
    The following instructions are to execute the tests of same functions
    If any test is fail, we will receive the notice when executing
    :return: None
    """
    doctest.run_docstring_examples(check_nulls, globals(), verbose=True)  # vemos los resultados de los test
    doctest.run_docstring_examples(ith, globals(), verbose=True)  # vemos los resultados de los test
    doctest.run_docstring_examples(isStress, globals(), verbose=False)  # solo los resultados de los test que fallan
    doctest.run_docstring_examples(summary, globals(), verbose=False)  # solo los resultados de los test que fallan


if __name__ == "__main__":
    test_doc()  # executing tests

