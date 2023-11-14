import pandas as pd
from .urlemt import UrlEMT
from io import StringIO

class BiciMad:
    """
    Representa los datos de uso de las bicicletas eléctricas de BiciMAD para un mes completo.
    Permite la limpieza y análisis básico de los datos.
    """

    def __init__(self, month: int, year: int) -> None:
        """
        Constructor para BiciMad.

        Parameters:
        --------
        month: int
            Mes de los datos.
        year: int
            Año de los datos.
        """

        self.validate_date(month, year)
        self._month = month
        self._year = year
        self._data = self.get_data(month, year)

    @staticmethod
    def validate_date(month: int, year: int):
        """
        Valida que el mes y el año sean correctos
        """
        if not 1 <= month <= 12:
            raise ValueError("El mes proporcionado no es válido. Debe estar entre 1 y 12.")
        if not 2000 <= year <= 2100:
            raise ValueError("El año proporcionado no es válido. Debe estar entre 2000 y 2100.")

    @staticmethod
    def get_data(month: int, year: int) -> pd.DataFrame:
        """
        Obtiene los datos de uso para el mes y año especificados.

        Parameters:
        --------
        month: int
            Mes de los datos.
        year: int
            Año de los datos.

        Returns:
        --------
        pd.DataFrame
            Un DataFrame con los datos de uso de las bicicletas.
        """
        BiciMad.validate_date(month, year)

        url_emt = UrlEMT()
        url_emt.select_valid_urls()

        try:
            csv_url = url_emt.get_url(month, year)
            csv_text = url_emt.get_csv(csv_url)
        except Exception as e:
            raise ValueError(f"No se pudo obtener los datos para el mes {month} y año {year}: {e}")

        try:
            data = pd.read_csv(StringIO(csv_text), sep=';', parse_dates=['unlock_date', 'lock_date'])
        except ValueError:
            raise ValueError("Error al leer el CSV. Asegúrate de que el formato del CSV es correcto.")

        BiciMad.validate_data_columns(data)

        data.set_index('unlock_date', inplace=True)

        return data

    @staticmethod
    def validate_data_columns(data: pd.DataFrame):
        required_columns = [
            'idBike', 'fleet', 'trip_minutes', 'geolocation_unlock', 'address_unlock',
            'locktype', 'unlocktype', 'geolocation_lock', 'address_lock', 'lock_date',
            'station_unlock', 'unlock_station_name', 'station_lock', 'lock_station_name'
        ]

        missing_columns = set(required_columns) - set(data.columns)
        if missing_columns:
            raise ValueError(f"Faltan las siguientes columnas esperadas en los datos: {missing_columns}")

        if 'unlock_date' not in data.columns or not pd.api.types.is_datetime64_any_dtype(data['unlock_date']):
            raise ValueError("Los datos CSV no contienen 'unlock_date' como una columna de fecha y hora válida.")

    @property
    def data(self) -> pd.DataFrame:
        """
        Proporciona acceso al DataFrame con los datos de uso.

        Returns:
        --------
        pd.DataFrame
            El DataFrame con los datos de uso.
        """
        return self._data

    def __str__(self) -> str:
        """
        Representa la clase BiciMad como una cadena que muestra el DataFrame.

        Returns:
        --------
        str
            Representación de cadena del DataFrame de uso.
        """
        return str(self._data)

    def clean(self) -> None:
        """
        Limpia y prepara el DataFrame para el análisis.
        """
        self._data.dropna(axis=0, how='all', inplace=True)
        self._data['fleet'] = self._data['fleet'].astype(str)
        self._data['idBike'] = self._data['idBike'].astype(str)

        # Convierte a string si las columnas existen
        for column in ['station_lock', 'station_unlock']:
            if column in self._data.columns:
                self._data[column] = self._data[column].astype(str)

        # Asegura que las fechas están en formato datetime si no lo están ya
        if not pd.api.types.is_datetime64_dtype(self._data.index):
            self._data.index = pd.to_datetime(self._data.index)

    def resume(self) -> pd.Series:
        """
        Resume las estadísticas fundamentales del uso de bicicletas para el mes y el año marcados.

        Returns:
        --------
        pd.Series
            Serie con estadísticas fundamentales del uso de bicicletas.
        """
        total_uses = len(self._data)
        total_time = self._data['trip_minutes'].sum() / 60
        most_popular_stations = self.most_popular_stations()
        uses_from_most_popular = self.usage_from_most_popular_unlock_station()

        return pd.Series({
            'year': self._year,
            'month': self._month,
            'total_uses': total_uses,
            'total_time': total_time,
            'most_popular_stations': most_popular_stations,
            'uses_from_most_popular': uses_from_most_popular
        })

    def most_popular_stations(self) -> set:
        """
        Identifica las estaciones de desbloqueo más populares.

        Returns:
        --------
        set:
            Conjunto con los nombres de las estaciones más populares.

        Examples:
        --------
        >>> bicimad = BiciMad(month=6, year=2021)
        >>> bicimad.most_popular_stations()
        {'Plaza Picasso', 'Santiago Bernabeu'}
        """
        conteo_estacion = self._data['unlock_station_name'].value_counts()
        max_value = conteo_estacion.max()
        return set(conteo_estacion[conteo_estacion == max_value].index)

    def usage_from_most_popular_unlock_station(self) -> int:
        """
        Calcula el número de usos de la estación de desbloqueo más popular.

        Returns:
        --------
        int:
            Número de usos de la estación de desbloqueo más popular.

        Examples:
        --------
        >>> bicimad = BiciMad(month=6, year=2021)
        >>> bicimad.usage_from_most_popular_unlock_station()
        532
        """
        most_popular = self.most_popular_stations()
        if not most_popular:
            return 0
        # Suponiendo que solo hay una estación más popular.
        # En caso contrario se puede modificar para poder devolver múltiples estaciones.
        return self._data[self._data['unlock_station_name'].isin(most_popular)].shape[0]

    def day_time(self) -> pd.Series:
        """
        Calcula las horas totales de uso de bicicletas por día del mes.

        Returns:
        --------
        pd.Series:
            Una serie donde el índice es la fecha y el valor es el número de horas.
        """
        self._data['trip_hours'] = self._data['trip_minutes'] / 60
        return self._data.resample('D')['trip_hours'].sum()

    def weekday_time(self) -> pd.Series:
        """
        Calcula las horas totales de uso de bicicletas por día de la semana.

        Returns:
        --------
        pd.Series:
            Una serie donde el índice es el día de la semana (L, M, X, J, V, S, D) y el valor es el número de horas.
        """
        if 'trip_hours' not in self._data.columns:
            self._data['trip_hours'] = self.data['trip_minutes'] / 60
        self._data['weekday'] = self._data.index.dayofweek
        days = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
        self._data['weekday'] = self._data['weekday'].map(days)
        uso_semanal = self._data.groupby('weekday')['trip_hours'].sum()
        return uso_semanal.reindex(['L', 'M', 'X', 'J', 'V', 'S', 'D'])

    def total_usage_day(self) -> pd.Series:
        """
        Calcula el número total de usos de bicicletas por día del mes.

        Returns:
        --------
        pd.Series:
            Serie con la fecha como índice y el número total de usos como valor.
        """
        return self._data.resample('D').size()



