import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv

from requests.cookies import create_cookie


def create_url_list(year, volume):
    """
    Create url_list of the journals by year and volume number
    Parameters
    ----------
    year : int
        year of journal
    volume : int
        volume of journal

    Returns
    -------
    url_list : list
        the list of journals' url_list
    """
    url = "https://www.journals.uchicago.edu/toc/jpe/"
    url_list = []
    for i in range(12, 0, -1):
        url_list.append(url + str(year) + '/' + str(volume) + '/' + str(i))
    return url_list


def translate_words(words):
    """
    Translate English to Chinese by using Youdao Translator API
    Parameters
    ----------
    words : str
        article title in English

    Returns
    -------
    translation : str
        the Chinese translation of article title
    """
    xml = requests.get(f"http://fanyi.youdao.com/translate?&i={words}&doctype=xml&version")
    root = ET.fromstring(xml.text)
    return root.find("./translation").text.replace(' ', '').replace('\n', '').replace('\r', '')


def save_titles(urls, filepath):
    """
    save journal's article titles to CSV file. Format: title, Chinese translation
    Parameters
    ----------
    urls : list
        the url list of journal
    filepath : str
        CSV file path and file name

    Returns
    -------

    """
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "translation"])
        for url in urls:
            html = requests.get(url)
            html.encoding = html.apparent_encoding
            content = html.text

            soup = BeautifulSoup(content, "html.parser")
            for i in soup.find_all('h5', class_="issue-item__title"):
                orig = i.get_text()
                translation = translate_words(orig)
                writer.writerow([orig, translation])
                print(orig, translation)
    csvfile.close()


if __name__ == "__main__":
    year_volume = [[2019, 127], [2020, 128], [2021, 129]]
    for i in year_volume:
        URLs = create_url_list(i[0], i[1])
        save_titles(URLs, f"./{i[0]}-{i[1]}.csv")
