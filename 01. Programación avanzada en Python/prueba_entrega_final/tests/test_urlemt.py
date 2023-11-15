import pytest
import requests_mock
from bicimad import UrlEMT
import io
import zipfile

@pytest.fixture
def html_response():
    """
    Proporciona una respuesta HTML de ejemplo que incluye etiquetas de anclaje con atributos href.
    Esto imita la estructura HTML de la página de datos abiertos de EMT Madrid que contiene enlaces a archivos CSV.
    """
    return """
    <a href="https://opendata.emtmadrid.es/getattachment/ab3776ab-ba7f-4da3-bea6-e70c21c7d8be/trips_21_06_June-csv.aspx">Junio 2021</a>
    <a href="https://opendata.emtmadrid.es/getattachment/abcdefgh-ijkl-mnop-qrst-uvwxyz123456/trips_21_07_July-csv.aspx">Julio 2021</a>
    """

def test_instance_creation():
    """
    Prueba la creación de una instancia de UrlEMT para asegurarse de que no sea None.
    """
    url_emt = UrlEMT()
    assert url_emt is not None

def test_get_links(html_response):
    """
    Prueba el método estático get_links de la clase UrlEMT.
    Verifica si el método extrae correctamente las URL válidas de la respuesta HTML proporcionada.
    """
    links = UrlEMT.get_links(html_response)
    assert "https://opendata.emtmadrid.es/getattachment/ab3776ab-ba7f-4da3-bea6-e70c21c7d8be/trips_21_06_June-csv.aspx" in links
    assert len(links) == 2

@pytest.fixture
def mock_request(requests_mock, html_response):
    """
    Simula una solicitud GET a la página de datos generales de EMT Madrid.
    Retorna la respuesta HTML de ejemplo cuando la clase UrlEMT solicita la URL.
    """
    requests_mock.get(UrlEMT.EMT + UrlEMT.GENERAL, text=html_response)
    return requests_mock

def test_select_valid_urls(mock_request):
    """
    Prueba el método select_valid_urls de la clase UrlEMT.
    Asegura que el método devuelve un conjunto con la cantidad correcta de URL válidas.
    """
    valid_urls = UrlEMT.select_valid_urls()
    assert len(valid_urls) == 2
    assert "https://opendata.emtmadrid.es/getattachment/ab3776ab-ba7f-4da3-bea6-e70c21c7d8be/trips_21_06_June-csv.aspx" in valid_urls

def test_get_url(mock_request):
    """
    Prueba el método get_url de la clase UrlEMT para asegurarse de que devuelve la URL correcta para un mes y año dados.
    """
    url_emt = UrlEMT()
    expected_url = "https://opendata.emtmadrid.es/getattachment/ab3776ab-ba7f-4da3-bea6-e70c21c7d8be/trips_21_06_June-csv.aspx"
    assert url_emt.get_url(6, 2021) == expected_url


def test_get_csv(mock_request, requests_mock):
    """
    Prueba el método get_csv de la clase UrlEMT.
    """
    csv_content = "idBike,fleet,trip_minutes,geolocation_unlock,address_unlock,lock_date\n"
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("trips_21_06_June-csv.csv", csv_content)

    zip_buffer.seek(0)
    requests_mock.get("https://opendata.emtmadrid.es/getattachment/ab3776ab-ba7f-4da3-bea6-e70c21c7d8be/trips_21_06_June-csv.aspx", content=zip_buffer.getvalue())

    url_emt = UrlEMT()
    url_emt.select_valid_urls()
    csv_text_io = url_emt.get_csv(6, 2021)  # Actualizado para usar mes y año en lugar de URL
    assert csv_text_io is not None
    assert csv_text_io.read() == csv_content
