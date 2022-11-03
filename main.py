import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv


def create_urls(year, volume):
    url = "https://www.journals.uchicago.edu/toc/jpe/"
    urls = []
    for i in range(12, 0, -1):
        urls.append(url + str(year) + '/' + str(volume) + '/' + str(i))
    return urls


def translate_words(words):
    xml = requests.get("http://fanyi.youdao.com/translate?&i={0}&doctype=xml&version".format(words))
    root = ET.fromstring(xml.text)
    return root.find("./translation").text.replace(' ', '').replace('\n', '').replace('\r', '')


def get_titles(urls, filepath):
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


urls = create_urls(2021, 129)  # 年份和期数
get_titles(urls, "./2020-128.csv")  # 要保存的路径和文件名
