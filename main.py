import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv


def create_ur_list(year, volume):
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
    Translate English to Chinese by using Youdao Translator API to
    Parameters
    ----------
    words : str
        article title in English

    Returns
    -------
    translation : str
        the Chinese translation of article title
    """
    xml = requests.get("http://fanyi.youdao.com/translate?&i={0}&doctype=xml&version".format(words))
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
    with open(filepath, "w", newline="") as csvfile:
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


urls = create_ur_list(2021, 129)  # 年份和期数
save_titles(urls, "./2020-128.csv")  # 要保存的路径和文件名
