import pandas as pd
import requests
from bs4 import BeautifulSoup
from .exception import *

EROGAME_SCAPE_SQL_URL = 'http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/sql_for_erogamer_form.php'


def execute(sql):
    http_responce = requests.post(EROGAME_SCAPE_SQL_URL, {'sql': sql})
    html = http_responce.content
    soup = BeautifulSoup(html, "lxml")
    #- error が出てるか確認
    message = soup.find(id='query_result_main').get_text()
    if message[:6] == 'ERROR:':
        raise SQLError(message)
    #-

    columns = [th.get_text()
               for th in soup.select('#query_result_main > table > tr > th')]
    data = [[td.get_text() for td in tds] for
            tds in [th.select('td') for th in soup.select('#query_result_main > table > tr')]][1:]
    df = pd.DataFrame(data, columns=columns)
    return df
