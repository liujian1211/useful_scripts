# import requests
# from bs4 import BeautifulSoup
#
# def get_credit_code(company_name):
#     # search_url = "https://www.qcc.com/web/search?key=" + company_name
#     search_url = 'https://www.qcc.com/web/search?key=%E5%B8%B8%E5%B7%9E%E8%8B%8F%E7%93%B7%E7%BA%B3%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8'
#     response = requests.get(search_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # 获取搜索结果列表的第一个公司的统一社会信用代码
#     result = soup.find("a", class_="ma_h1")
#     if result:
#         company_url = "https://www.qcc.com" + result['href']
#         company_response = requests.get(company_url)
#         company_soup = BeautifulSoup(company_response.text, 'html.parser')
#         credit_code = company_soup.find("td", text="统一社会信用代码：").find_next("td").text.strip()
#         return credit_code
#     else:
#         return "未找到统一社会信用代码"
#
# # 假设你的公司列表存储在一个名为companies的列表中
# companies = ["常州苏瓷纳米科技有限公司"]
#
# for company in companies:
#     credit_code = get_credit_code(company)
#     print(f"{company}的统一社会信用代码是：{credit_code}")

import requests
import json
import time
from hashlib import md5

# 获取时间戳
def get_time_tup():
    """
    :return: 13位精确到秒的时间戳
    """
    time_tup = str(int(time.time()))
    return time_tup


# md5加密
def set_md5(s):
    """
    :param s: 拼接的字符串
    :return: md5加密再转化为大写的字符串
    """
    new_md5 = md5()
    new_md5.update(s.encode(encoding='utf-8'))
    s_md5 = new_md5.hexdigest().upper()
    return s_md5

# 设置请求头
def get_headers(key, screat_key):
    """
    :param key: 我的key
    :param screat_key: 我的密钥
    :return: 请求头
    """
    headers = dict()
    token = key + get_time_tup() + screat_key
    headers["Token"] = set_md5(token)
    headers["Timespan"] = get_time_tup()
    return headers


# 批量申请数据

def get_data(codes, name, key, screat_key):
    """
    :param codes: 关键字的可迭代对象
    :param name: 存储文档的署名
    :param key:  我的key
    :param screat_key: 我的密钥
    :return:  无
    """
    with open(f"data_{name}.csv", "w") as f, open(f"error_data_{name}.csv", "w") as f2:
        count = 0
        count_true = 0
        count_false = 0
        for code in codes:
            try:
                count += 1
                url = f"http://api.qichacha.com/ECIV4/GetBasicDetailsByName?key={key}&keyword={code}"
                s = requests.get(url=url, headers=get_headers(key, screat_key))
                t = s.text
                m = json.loads(t)
                print(m)
                if m["Status"] == "200":
                    x = m["Result"]
                    f.write(str(x["KeyNo"]) + '~' + str(x["Name"]) + '~'
                            + str(x["No"]) + '~' + str(x["BelongOrg"]) + '~'
                            + str(x["OperName"]) + '~' + str(x["StartDate"]) + '~'
                            + str(x["EndDate"]) + '~' + str(x["Status"]) + '~'
                            + str(x["Province"]) + '~' + str(x["UpdatedDate"]) + '~'
                            + str(x["CreditCode"]) + '~' + str(x["RegistCapi"]) + '~'
                            + str(x["EconKind"]) + '~' + str(x["Address"]) + '~'
                            + str(x["Scope"]) + '~' + str(x["TermStart"]) + '~'
                            + str(x["TeamEnd"]) + '~' + str(x["CheckDate"]) + '~'
                            + str(x["OrgNo"]) + '~' + str(x["IsOnStock"]) + '~'
                            + str(x["StockNumber"]) + '~' + str(x["StockType"])
                            + "\n")
                    count_true += 1
                else:
                    f2.write(code)
                    f2.write("\n")
                    count_false += 1
            except:
                f2.write(code)
                f2.write("\n")
                count_false += 1
        print("匹配到的数据", count_true)
        print("未匹配到的数据", count_false)
        print("数据总数", count)


if __name__ == '__main__':
    # 此处需要自己调整
    codes = data["企业名称"]
    key = '我的key'
    screat_key = '我的密钥'
    get_data(codes, "example", key, screat_key)

