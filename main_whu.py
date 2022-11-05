import requests
from bs4 import BeautifulSoup
import csv

def create_url_list(year, volume):
    """create url list of WHU GIS journal archive

    Parameters
    ----------
    year : int
        the year of journal
    volume : int
        volumes of point year

    Returns
    -------
    list
        url list
    """
    url = "http://ch.whu.edu.cn/cn/article/"
    url_list = []
    for i in range(1, volume+1):
        tmp = url + f"{year-1}/{i}"
        url_list.append(tmp)
    
    return url_list


def extract_article_info(url):
    """extract articles infomation in a volume of journal

    Parameters
    ----------
    url : str
        a volume archive of journal
    """
    articles_info = []
    html = requests.get(url)
    html.encoding = html.apparent_encoding
    content = html.text
    soup = BeautifulSoup(content, "html.parser")
    for article in soup.find_all(class_="article-list-title"):
        orig = article.get_text()
        print(orig)
        
    


if __name__ == "__main__":
    URLs = create_url_list(2022, 9)
    for url in URLs:
        extract_article_info(url)


