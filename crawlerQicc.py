# -*- coding-8 -*-
import requests
import lxml
from bs4 import BeautifulSoup
import xlwt
import re
import urllib
import random
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
def get_user_agent():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    ]
    uer_agent = random.choice(user_agent_list)
    return uer_agent

def craw(url):
    headers = {
        'Host': 'www.qichacha.com',
        'User-Agent': get_user_agent(),
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.qichacha.com/',
        'Cookie': r'UM_distinctid***************',
        'Connection': 'keep-alive',
        'If-Modified-Since': 'Wed, 30 **********',
        'If-None-Match': '"59*******"',
        'Cache-Control': 'max-age=0',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        response.encoding = 'utf-8'
        print(response.status_code)
        print('ERROR')
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    com_names = soup.find_all(class_='ma_h1')
    print(com_names)
    res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
    link = re.findall(res_url, str(com_names), re.I | re.S | re.M)
    return link[0]

def crawler_company(url,company):
    request = urllib.request.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, 'lxml')
    print(soup)
    context = str(soup)
    print(context)
    path = "F:/eclipse/eclipse-workspace/cia_web/file/company/企查查/" + company +".html"
    file = open(path,"wb")
    file.write(context.encode("utf-8"))
    file.close()

if __name__ == '__main__':
    f = open("./company.txt")
    key_word = f.read()
    f.close()
    print('正在搜索，请稍后')
    url = r'http://www.qichacha.com/search?key={}#p:{}&'.format(key_word, 1)
    s1 = craw(url)
    url_company = "http://www.qichacha.com" + s1
    print(url_company)
    crawler_company(url_company,key_word)
