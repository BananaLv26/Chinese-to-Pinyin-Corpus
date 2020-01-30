import requests
import random
import codecs
import json
from bs4 import BeautifulSoup

requests.adapters.DEFAULT_RETRIES = 5
DOWNLOAD_URL = 'https://so.gushiwen.org/shiwen/default_0AA1.aspx'


def download_page(url):
    user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) "
        "Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) "
        "Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; ."
        "NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    ]
    # 随机获取一个浏览器
    rand_agent = random.choice(user_agent)
    # 拼装请求头
    header = {
        "User-Agent": rand_agent,
    }

    data = requests.get(url, headers=header, timeout=5).content
    return data


def parseHtml(html):
    soup = BeautifulSoup(html, features="html.parser")
    #    nextPage = 'https://so.gushiwen.org' + soup.find('a', attrs={'class': 'amore'}).get('href')
    leftDiv = soup.find('div', attrs={'class': 'main3'}).find('div', attrs={'class': 'left'})
    find_nextpage = leftDiv.find('form', attrs={'id': 'FromPage'}).find('div', attrs={'class': 'pagesright'})
    nextPage = 'https://so.gushiwen.org' + find_nextpage.find('a', attrs={'class': 'amore'}).get('href')

    all = soup.find('div', attrs={'class': 'main3'}).find('div', attrs={'class': 'left'})
    return all, nextPage


def buildJson(keys, values):
    dictionary = dict(zip(keys, values))
    return json.dumps(dictionary)


def ParsePoemHtml(all):
    output = []
    for son in all.find_all('div', attrs={'class': 'sons'}):
        title = son.find('div', attrs={'class': 'cont'}).find('b').getText()
        content = son.find('div', attrs={'class': 'cont'}).find('div', attrs={'class': 'contson'}).getText().strip()
        output.append(title + '。' + content)
    return output


# def parseAuthorMore(html):
# #     soup = BeautifulSoup(html, features='html.parser')
# #     yishi = []
# #     if soup.find('div', attrs={'clase', 'contyishang'}):
# #         for p in soup.find('div', attrs={'clase', 'contyishang'}).find_all('p'):
# #             yishi.append(p.getText())
# #     return ''.join(yishi)
def buildJson(keys, values):
    dictionary = dict(zip(keys, values))
    return json.dumps(dictionary)


def save(filename, docs):
    f = open(filename, 'w', encoding='utf-8')
    for doc in docs:
        f.write(doc)
        f.write('\n')
    f.close()


def main():
    url = DOWNLOAD_URL
    keys = ['content']
    f = open('poem.txt', 'w', encoding='utf-8')
    while url:
        html = download_page(url)
        all, url = parseHtml(html)
        output = ParsePoemHtml(all)

        for doc in output:
            f.write(doc)
            f.write('\n')
    f.close()


if __name__ == '__main__':
    main()

