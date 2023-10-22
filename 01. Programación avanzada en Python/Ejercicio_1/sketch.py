"""
Program to analize the logs files of an apache server.
An example of file acommpanies this file: access.log
"""

import re
import doctest

def get_user_agent(line: str) -> str:
    """
    Busca cualquier cosa entre comillas dobles al final de la línea.
    Si encuentra una coincidencia, devuelve el contenido; si no devuelve una cadena vacía.

    Expamples
    ---------
    >>> get_user_agent('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    >>> get_user_agent('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
    """
    match = re.search(r'"([^"]+)"$', line)
    if match:
        return match.group(1)
    return ""


def is_bot(line: str) -> bool:
    '''
    Determina si la línea de registro pertenece a un bot.
    Devuelve el booleano 'True' si se trata de un bot o 'False' en caso contrario.

    Examples
    --------
    >>> is_bot('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    False

    >>> is_bot('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    True

    >>> is_bot('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    True
    '''
    user_agent = get_user_agent(line).lower()
    return 'bot' in user_agent


def get_ipaddr(line: str) -> str:
    '''
    Obtiene la dirección IP de la línea.

    >>> get_ipaddr('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    '213.180.203.109'

    >>> get_ipaddr('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    '147.96.46.52'
    '''
    return line.split()[0]


def get_hour(line: str) -> int:
    """
    Extrae la hora de una línea del registro.

    Args:
    line (str): Una cadena del archivo de registro. -1 si no se encuentra la hora.

    Returns:
    int: La hora en la que ocurrió el acceso.

    Expamples
    ---------
    >>> get_hour('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    0

    >>> get_hour('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antacres.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    12
    """
    match = re.search(r'\[.*:(\d{2}):\d{2}:\d{2} .*]', line)
    if match:
        return int(match.group(1))
    else:
        return -1


def histbyhour(filename: str) -> dict[int, int]:
    '''
    Genera un histórico de accesos por hora a partir de un registro.

    Args:
    filename (str): la ruta del archivo de registro.

    Returns:
    Dict[int, int]: Un diccionario con las horas únicas como claves y sus correspondientes cantidades de accesos como valores.
    '''
    hist = {}
    try:
        with open(filename) as f:
            for line in f:
                hour = get_hour(line)
                hist[hour] = hist.get(hour, 0) + 1
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    return hist


def ipaddreses(filename: str) -> set[str]:
    '''
    Devuelve las IPs de los accesos que no son bots.

    Args:
    filename (str): la ruta del archivo de registro.

    Returns:
    Set[str]: un conjunto de direcciones IP.
    '''
    ip_set = set()
    try:
        with open(filename) as f:
            for line in f:
                if not is_bot(line):
                    ip_set.add(get_ipaddr(line))
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    return ip_set


def main():
    # Prueba de las funciones con doctests
    test_doc()

    # Prueba de la función ipaddreses
    test_ipaddresses()

    # Prueba de la función histbyhour
    test_hist()

    print("Todas las pruebas se han ejecutado correctamente.")


def test_doc():
    doctest.run_docstring_examples(get_user_agent, globals(), verbose=True)
    doctest.run_docstring_examples(is_bot, globals(), verbose=True)
    doctest.run_docstring_examples(get_ipaddr, globals(), verbose=True)
    doctest.run_docstring_examples(get_hour, globals(), verbose=True)

def test_ipaddresses():
    assert ipaddreses('access_short.log') == {'34.105.93.183', '39.103.168.88'}

def test_hist():
    hist = histbyhour('access_short.log')
    assert hist == {5: 3, 7: 2, 23: 1}

if __name__ == "__main__":
    main()