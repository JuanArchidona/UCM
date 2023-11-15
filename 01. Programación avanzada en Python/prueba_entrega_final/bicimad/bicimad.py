import pandas as pd
from bicimad import UrlEMT
from typing import Set

class BiciMad:
    """
    Representa los datos de uso de las bicicletas eléctricas de BiciMAD para un mes completo.
    Permite la limpieza y análisis básico de los datos.
    """

    def __init__(self, month: int, year: int) -> None:
        """
        Constructor de la clase BiciMad.

        Parameters:
        --------
        month: int
            Mes de los datos.
        year: int
            Año de los datos.
        """
        self._month = month
        self._year = year
        self._data = self.get_data(month, year)

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
        url_emt = UrlEMT()
        csv_text_io = url_emt.get_csv(month, year)
        df = pd.read_csv(csv_text_io, parse_dates=['unlock_date', 'lock_date'], dayfirst=True)
        df.set_index('unlock_date', inplace=True) # Damos por válido que unlock_date es la fecha del viaje
        return df

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
        self._data.dropna(how='all', inplace=True)
        self._data[['fleet', 'idBike', 'station_lock', 'station_unlock']] = self._data[['fleet', 'idBike', 'station_lock', 'station_unlock']].astype(str)


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

        summary = pd.Series({
            'year': self._year,
            'month': self._month,
            'total_uses': total_uses,
            'total_time': total_time,
            'most_popular_stations': most_popular_stations,
            'uses_from_most_popular': uses_from_most_popular
        })
        return summary

    def most_popular_stations(self) -> Set[str]:
        """
        Identifica las estaciones de desbloqueo más populares.

        Returns:
        --------
        set:
            Conjunto con los nombres de las estaciones más populares.
        """
        conteo_estacion = self._data.groupby('unlock_station_name').size()
        maximo_viajes = conteo_estacion.max()
        estaciones_mas_populares = set(conteo_estacion[conteo_estacion == maximo_viajes].index)
        return estaciones_mas_populares

    def usage_from_most_popular_unlock_station(self) -> int:
        """
        Calcula el número de usos de la estación de desbloqueo más popular.

        Returns:
        --------
        int:
            Número de usos de la estación de desbloqueo más popular.
        """
        conteo_estacion = self._data.groupby('station_unlock').size()
        maximo_viajes = conteo_estacion.max()
        return maximo_viajes

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
            self._data['trip_hours'] = self._data['trip_minutes'] / 60
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
