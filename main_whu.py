import requests
from bs4 import BeautifulSoup
import csv


def create_url_list(year):
    """create url list of WHU GIS journal archive

    Parameters
    ----------
    year : int
        the year of journal

    Returns
    -------
    list
        url list
    """
    if year == 2022:
        volume = 9
    else:
        volume = 12
    url = "http://ch.whu.edu.cn/cn/article/"
    url_list = []
    for i in range(1, volume + 1):
        tmp = url + f"{year - 1}/{i}"
        url_list.append(tmp)

    return url_list


def extract_article_info(url):
    """extract articles information in a volume of journal

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
    for article in soup.find_all(class_="article-list-right"):
        title = article.find(class_="article-list-title").get_text().replace("\n", "")
        tmp = article.find("font", class_="font2 count1")
        if tmp:
            link = tmp.find("a").get("href")
        else:
            link = []

        articles_info.append([title, link])
        print(f"成功获取： {title} 文章地址：{link}")

    return articles_info


def save_to_csv(article_info, file_path):
    """save article info to CSV file, formatting as [title, article link]

    Parameters
    ----------
    article_info : list
        list of articles
    file_path : str
        the file path of CSV to save
    """
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "link"])
        for info in article_info:
            writer.writerow([info[0], info[1]])
    csvfile.close()
    print("文件:{0}写入成功！".format(file_path.replace("./", "")))


if __name__ == "__main__":
    years = [2018, 2019, 2020, 2021, 2022]
    for year in years:
        url_list = create_url_list(year)
        for url, i in zip(url_list, range(len(url_list) + 1)):
            article_info = extract_article_info(url)
            file_path = f"./WHUcsv/{year}年-第{i + 1}期.csv"
            save_to_csv(article_info, file_path)
