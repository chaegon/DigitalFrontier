import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_index():
    url = "https://finance.naver.com/sise/"
    result = requests.get(url)
    html = BeautifulSoup(result.content, "html.parser")

    index_info = {"kospi_value": html.find("span", {"class": "num", "id": "KOSPI_now"}).string
        , "kospi_change": html.find("span", {"class": "num_s", "id": "KOSPI_change"}).text.split(' ')[0]
        , "kospi_changepc": html.find("span", {"class": "num_s", "id": "KOSPI_change"}).text.split(' ')[1].split('%')[0]

        , "kosdaq_value": html.find("span", {"class": "num", "id": "KOSDAQ_now"}).string
        , "kosdaq_change": html.find("span", {"class": "num_s", "id": "KOSDAQ_change"}).text.split(' ')[0]
        , "kosdaq_changepc": html.find("span", {"class": "num_s", "id": "KOSDAQ_change"}).text.split(' ')[1].split('%')[
            0]

        , "kpi200_value": html.find("span", {"class": "num", "id": "KPI200_now"}).string
        , "kpi200_change": html.find("span", {"class": "num_s", "id": "KPI200_change"}).text.split(' ')[0]
        , "kpi200_changepc": html.find("span", {"class": "num_s", "id": "KPI200_change"}).text.split(' ')[1].split('%')[
            0]
                  }

    return index_info

index = get_index()
print(index["kosdaq_value"])