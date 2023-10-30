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

  Raises:
  --------
  FileNotFoundError:
    El archivo no se encuentra
  Exception:
    Otros tipos de errores no descritos durante la lectura del archivo

  Examples:
  --------
  >>> read_data('zonas.txt', int)
  array([[1, 1, 1, 1, 3, 3],
         [1, 1, 1, 1, 3, 1],
         [2, 2, 3, 3, 3, 4],
         [2, 2, 3, 3, 3, 4],
         [2, 2, 3, 3, 2, 2],
         [3, 3, 3, 3, 3, 2]])

  >>> read_data('valores.txt', float)
  array([[5., 3., 4., 4., 4., 2.],
         [2., 1., 4., 2., 6., 3.],
         [8., 4., 3., 5., 3., 1.],
         [4., 2., 4., 3., 2., 2.],
         [6., 3., 3., 7., 4., 2.],
         [5., 5., 2., 3., 1., 3.]])

  >>> read_data('archivo_que_no_existe.txt', int) # doctest: +IGNORE_EXCEPTION_DETAIL
  Traceback (most recent call last):
  ...
  FileNotFoundError: no se encontró el archivo archivo_que_no_existe.txt
  """
  try:
    return np.loadtxt(fname, dtype=tipo)
  except FileNotFoundError:
      raise FileNotFoundError(f'no se encontró el archivo {fname}')
  except Exception as e:
      raise Exception(f'Error al leer el archivo {fname}: {e}')

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
        raise TypeError(f"The elements type must be int, not {zonas.dtype}")
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

    Examples:
    --------
    >>> zonas = np.array([[1, 1], [2, 2]], dtype=np.int_)
    >>> valores = np.array([[10, 20], [30, 40]], dtype=np.int_)
    >>> mean_areas(zonas, valores)
    array([[15., 15.],
           [35., 35.]])
    >>> zonas = np.array([[1, 1], [1, 1]], dtype=np.int_)
    >>> valores = np.array([[10, 20], [30, 40]], dtype=np.int_)
    >>> mean_areas(zonas, valores)
    array([[25., 25.],
           [25., 25.]])
    >>> zonas = np.array([[1, 2], [3, 4]], dtype=np.int_)
    >>> valores = np.array([[10, 20], [30, 40]], dtype=np.int_)
    >>> mean_areas(zonas, valores)
    array([[10., 20.],
           [30., 40.]])
    >>> zonas = np.array([[1, 1], [2, 2]], dtype=np.int_)
    >>> valores = np.array([[10, 20, 30], [30, 40, 50]], dtype=np.int_)
    >>> mean_areas(zonas, valores) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    IndexError: Input arrays must have the same dimensions
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
