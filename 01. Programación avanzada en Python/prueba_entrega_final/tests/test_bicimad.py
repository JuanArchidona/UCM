import pytest
from bicimad.bicimad import BiciMad
import pandas as pd
from io import StringIO


# Datos de prueba en formato CSV
CSV_TEST_DATA = """unlock_date;idBike;fleet;trip_minutes;geolocation_unlock;address_unlock;lock_date;station_lock;lock_station_name;unlock_station_name;...
2021-06-01 07:00;123;1;15;POINT(-3.70379 40.416775);Calle de Alcalá;2021-06-01 07:15;42;Estación 42;Estación A;...
2021-06-01 07:10;456;1;30;POINT(-3.70379 40.416775);Gran Vía;2021-06-01 07:40;58;Estación 58;Estación B;...
"""

@pytest.fixture
def bicimad_instance():
    """
    Proporciona una instancia de la clase BiciMad preparada con datos de prueba para junio de 2021.
    La llamada al método estático `get_data` se simula para que devuelva un DataFrame basado en CSV_TEST_DATA.
    """
    BiciMad.get_data = staticmethod(lambda month, year: pd.read_csv(StringIO(CSV_TEST_DATA), sep=';', parse_dates=['unlock_date', 'lock_date']))
    return BiciMad(6, 2021)

def test_instance_creation(bicimad_instance):
    """
    Verifica la correcta creación de una instancia de BiciMad y la asignación de atributos de mes y año.
    """
    assert bicimad_instance is not None
    assert bicimad_instance._month == 6
    assert bicimad_instance._year == 2021

def test_data_loading(bicimad_instance):
    """
    Comprueba que la carga de datos en la instancia de BiciMad genera un DataFrame no vacío.
    """
    data = bicimad_instance.data
    assert isinstance(data, pd.DataFrame)
    assert not data.empty

def test_clean_data(bicimad_instance):
    """
    Verifica que el método 'clean' de la clase BiciMad funcione correctamente,
    asegurando que los tipos de datos sean los correctos y que no haya valores NaN innecesarios.
    """
    bicimad_instance.clean()
    data = bicimad_instance.data
    assert data['fleet'].dtype == object
    assert data['idBike'].dtype == object
    assert data.isna().sum().sum() == 0

def test_resume(bicimad_instance):
    """
    Verifica que el resumen proporcionado por el método 'resume' de la clase BiciMad sea correcto.
    Comprueba las claves y algunos valores específicos del resumen.
    """
    resume = bicimad_instance.resume()
    assert isinstance(resume, pd.Series)
    expected_keys = {'year', 'month', 'total_uses', 'total_time', 'most_popular_station', 'uses_from_most_popular'}
    assert set(resume.index) == expected_keys - {'most_popular_station'} | {'most_popular_stations'}
    assert resume['total_uses'] == 2
    assert resume['total_time'] == 45 / 60

