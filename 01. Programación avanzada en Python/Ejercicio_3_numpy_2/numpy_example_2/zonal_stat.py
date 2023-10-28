import numpy as np


def read_data(fname: str, tipo: type) -> np.ndarray:
  """
  Lee los datos de un fichero y devuelve un array de numpy.

  Parameters:
  --------
  fname: str
    Ruta del archivo.
  tipo: type
    Tipo de dato del array resultante.

  Returns:
  --------
  np.ndarray
    Array con los datos leídos del archivo.
  """
  return np.loadtxt(fname, dtype=tipo)


def set_of_areas(zonas: np.ndarray)-> set[int]:
    """
    Establece las distintas zonas en un array y las devuelve en conjunto.

    Parameters:
    --------
    zonas: np.ndarray
        Array que muestra las zonas.

    Returns:
    --------
    set[int]
        Conjunto con las distintas zonas.

    Raises:
    --------
    TypeError:
        Si los elementos del array no son de tipo int.

    Examples:
    --------
    >>> set_of_areas(np.arange(10).reshape(5, 2))
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    >>> set_of_areas(np.zeros(10, dtype=np.int_).reshape(5, 2))
    {0}
    >>> set_of_areas(np.array([2, 3, 4, 2, 3, 4], dtype=np.int_).reshape(3, 2))
    {2, 3, 4}
    >>> set_of_areas(np.zeros(3, dtype=np.float_))
    Traceback (most recent call last):
        ...
    TypeError: The elements type must be int, not float64
    """
    if zonas.dtype != np.int_:
        raise TypeError(f"The elements type must be int not {zonas.dtype}")
    return set(zonas.flatten())


def mean_areas(zonas: np.ndarray, valores: np.ndarray) -> np.ndarray:
    """
    Calcula la media de las zonas geográficas.

    Parameters:
    --------
    zonas: np.ndarray
        Datos que representan las zonas geográficas.
    valores: np.ndarray
        Valores de las celdas del área total.

    Returns:
    --------
    np.ndarray
        Array con las medias calculadas por zona.

    Raises:
    --------
    IndexError
        Si los arrays de entrada no tienen las mismas dimensiones.
    """
    if zonas.shape != valores.shape:
        raise IndexError("Input arrays must have the same dimensions")

    unique_zones = set_of_areas(zonas)
    result = np.zeros_like(valores, dtype=np.float_)
    for zone in unique_zones:
        mask = zonas == zone
        mean_value = valores[mask].mean()
        result[mask] = round(mean_value, 1)
    return result


# ------------ test  --------#
import doctest

def test_doc()-> None:
    """
    The following instructions are to execute the tests of same functions
    If any test is fail, we will receive the notice when executing
    :return: None
    """
    doctest.run_docstring_examples(read_data, globals(), verbose=True)  # vemos los resultados de los test que fallan
    doctest.run_docstring_examples(set_of_areas, globals(), verbose=True)  # vemos los resultados de los test que fallan
    doctest.run_docstring_examples(mean_areas, globals(), verbose=True)  # vemos los resultados de los test que fallan


if __name__ == "__main__":
    test_doc()   # executing tests
