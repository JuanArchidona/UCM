import pytest
from bicimad import BiciMad
import pandas as pd
from io import StringIO

# Mock data para pruebas
MOCK_CSV_DATA = """unlock_date,trip_minutes,unlock_station_name,station_unlock,fleet,idBike,lock_date,station_lock
2021-06-01 08:00,30,Estación 1,1,100,1234,2021-06-01 08:30,2
2021-06-02 09:00,45,Estación 2,2,100,5678,2021-06-02 09:45,3
"""

@pytest.fixture
def mock_csv_data():
    return StringIO(MOCK_CSV_DATA)

@pytest.fixture
def bicimad_instance(mock_csv_data):
    # Mock la función get_csv para devolver los datos mock
    BiciMad.get_data = lambda self, month, year: pd.read_csv(
        mock_csv_data,
        parse_dates=['unlock_date', 'lock_date'],
        index_col='unlock_date'
    )
    return BiciMad(6, 2021)

def test_instance_creation(bicimad_instance):
    """Verifica la correcta creación de una instancia de BiciMad,
    incluyendo la correcta inicialización de su DataFrame con datos de prueba."""
    assert bicimad_instance is not None
    assert isinstance(bicimad_instance.data, pd.DataFrame)
    assert isinstance(bicimad_instance.data.index, pd.DatetimeIndex)
    assert len(bicimad_instance.data) == 2  # Basado en MOCK_CSV_DATA

def test_clean(bicimad_instance):
    """
    Prueba el método de limpieza de la clase BiciMad para asegurarse de que maneja adecuadamente los datos nulos o faltantes.
    """
    bicimad_instance.clean()
    assert 'NaN' not in bicimad_instance.data.values

def test_resume(bicimad_instance):
    """
    Comprueba la funcionalidad del método resume, asegurándose de que proporcione un resumen adecuado de los datos de uso de bicicletas.
    """
    summary = bicimad_instance.resume()
    assert summary['total_uses'] == 2
    assert summary['most_popular_stations'] == {'Estación 1', 'Estación 2'}
    assert summary['uses_from_most_popular'] == 1

def test_day_time(bicimad_instance):
    """
    Verifica que el método day_time de BiciMad calcule correctamente el uso total de bicicletas por día.
    """
    day_usage = bicimad_instance.day_time()
    assert len(day_usage) > 0

def test_weekday_time(bicimad_instance):
    """
    Evalúa si el método weekday_time proporciona correctamente el uso total de bicicletas por día de la semana.
    """
    weekday_usage = bicimad_instance.weekday_time()
    assert len(weekday_usage) > 0
    assert 'L' in weekday_usage.index

def test_total_usage_day(bicimad_instance):
    """
    Examina si el método total_usage_day de BiciMad cuenta correctamente el uso total de bicicletas por día.
    """
    total_usage = bicimad_instance.total_usage_day()
    assert len(total_usage) > 0
