import re
import requests
import io
import zipfile
from typing import TextIO, Set

class UrlEMT:
    EMT = 'https://opendata.emtmadrid.es/'
    GENERAL = "/Datos-estaticos/Datos-generales-(1)"

    def __init__(self):
        """
        Constructor de la clase UrlEMT. Inicializa el conjunto de enlaces encontrados en la web de EMT.
        """
        self._valid_urls = self.select_valid_urls()

    @staticmethod
    def get_links(html_text: str) -> Set[str]:
        """
        Extrae todos los enlaces válidos de un texto HTML.

        Parameters:
        --------
        html_text: str
            Texto HTML del que extraer los enlaces.

        Returns:
        --------
        Set[str]:
            Conjunto de enlaces válidos encontrados.
        """
        # Expresión regular para encontrar enlaces que contengan 'movements' y terminen en '.aspx'
        links = re.findall(r'href="(https://opendata.emtmadrid.es/getattachment/[a-z0-9-]+/trips_\d{2}_\d{2}_[A-Za-z]+-csv\.aspx)"', html_text)
        return set(links)

    @staticmethod
    def select_valid_urls() -> Set[str]:
        """
        Actualiza y devuelve el conjunto de enlaces válidos encontrados en la web de EMT.

        Returns:
        --------
        Set[str]:
            Conjunto de enlaces válidos.

        Raises:
        --------
        ConnectionError:
            Si la consulta a EMT falla.
        """
        response = requests.get(UrlEMT.EMT + UrlEMT.GENERAL)
        if response.status_code != 200:
            raise ConnectionError("No se puede acceder a la página de la EMT")
        return UrlEMT.get_links(response.text)

    def get_url(self, month: int, year: int) -> str:
        """
        Devuelve la URL correspondiente al mes y año introducidos.

        Parameters:
        --------
        month: int
            Mes seleccionado.
        year: int
            Año seleccionado.

        Returns:
        --------
        str:
            URL seleccionada.

        Raises:
        --------
        ValueError:
            Si el mes o el año no son válidos, o si no se encuentra la URL correspondiente.
        """
        if not (1 <= month <= 12):
            raise ValueError("Mes no válido")
        if not (21 <= year % 100 <= 2023):
            raise ValueError("Año no válido")

        month_name = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                      7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}[month]
        expected_part = f"trips_{year % 100:02}_{month:02}_{month_name}-csv.aspx"

        for url in self._valid_urls:
            if expected_part in url:
                return url
        raise ValueError("No se encuentra una URL válida para el mes y año dados")


    def get_csv(self, month: int, year: int) -> TextIO:
        """
        Devuelve un objeto TextIO representando el contenido de un archivo CSV.

        Parameters:
        --------
        month: int
            Mes deseado.
        year: int
            Año deseado.

        Returns:
        --------
        TextIO:
            Objeto TextIO con el contenido del archivo CSV.

        Raises:
        --------
        ConnectionError:
            Si la consulta al servidor EMT falla.
        """
        url = self.get_url(month, year)
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError("No se puede descargar el archivo")

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            csv_filename = z.namelist()[0]
            with z.open(csv_filename) as csv_file:
                return io.StringIO(csv_file.read().decode('utf-8'))
