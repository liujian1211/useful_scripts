# 扫码版
import re
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.common.by import By

credit_code = []
registered_capital = []
juridical_person = []
industry = []
business_scope = []
registered_address = []
enterprise_scale = []

check_dict = {
    "统一社会信用代码": credit_code,
    "注册资本": registered_capital,
    "法定代表人/负责人": juridical_person,
    "所属行业": industry,
    "经营范围": business_scope,
    "注册地址": registered_address,
    "企业规模": enterprise_scale,  # 企业规模
}


def get_company_url():
    path = "company_msg.xlsx"
    data = pd.read_excel(
        path, sheet_name=0
    )  # 默认读取第一个sheet的全部数据,int整数用于引用的sheet的索引（从0开始）

    option = webdriver.ChromeOptions()
    option.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )  # webdriver防检测

    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-usage")
    driver = webdriver.Chrome(options=option)
    # Selenium执行cdp命令，加了就不会有验证码
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
    })
    driver.set_page_load_timeout(25)
    driver.delete_all_cookies()
    url = (
        "https://www.qcc.com/weblogin?back=%2F"  # https://www.qcc.com/weblogin?back=%2F
    )
    driver.get(url)
    time.sleep(20)  # 扫码等待时间数字是秒

    company_urls = []

    for index, row in data.iterrows():
        name = str(row["入驻企业"]).strip()
        print(f"公司名称：{name}")
        if "公司" in name:
            name = re.findall("^.*?公司", name)[0]  # 排除曾用名的

        if name == "nan" or not name:
            company_urls.append("")
            continue
        try:
            driver.get(
                f"https://www.qcc.com/web/search?key={name}"
            )  # https://www.qcc.com/web/search?key={}
            try:
                d = driver.find_element(
                    By.XPATH,
                    "/html/body/div/div[2]/div[2]/div[3]/div/div[2]/div/table/tr[1]/td[3]/div/div[1]/span[1]/a",
                )
                txt = driver.find_element(
                    By.XPATH,
                    "/html/body/div/div[2]/div[2]/div[3]/div/div[2]/div/table/tr[1]/td[3]/div/div[1]/span[1]/a/span",
                )
                # 模糊查询，路径改为这个 /html/body/div/div[2]/div[2]/div[4]/div/div[2]/div/table/tr[1]/td[3]/div/div[1]/span[1]/a/span
                url = d.get_attribute("href")
                print(f"{txt.text}----->>>{url}")

                if txt.text == name:
                    company_urls.append(url)
                else:
                    print(f"查询名字：{name} --不一致---> 企查查名字：{txt.text}")
                    company_urls.append("")

            except NoSuchElementException:
                print(f"没找到该公司--->{name}")
                company_urls.append("")
                continue
            time.sleep(2)
        except:
            company_urls.append("")
            continue

    data["url"] = company_urls
    data.to_excel(path, index=None)


def get_company_msg():
    path = "company_msg.xlsx"
    data = pd.read_excel(
        path, sheet_name=0
    )  # 默认读取第一个sheet的全部数据,int整数用于引用的sheet的索引（从0开始）

    option = webdriver.ChromeOptions()
    option.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )  # webdriver防检测

    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-usage")
    driver = webdriver.Chrome(options=option)  # windows使用, chromedriver 链接放在同一个目录
    # driver = webdriver.Chrome(executable_path=r"/usr/bin/chromedriver", options=option)  # linux使用
    driver.set_page_load_timeout(25)
    driver.delete_all_cookies()
    url = (
        "https://www.qcc.com/weblogin?back=%2F"  # https://www.qcc.com/weblogin?back=%2F
    )

    driver.get(url)
    time.sleep(20)  # 扫码等待时间数字是秒

    for index, row in data.iterrows():
        url = str(row["url"]).strip()
        try:
            driver.get(url)  # https://www.qcc.com/web/search?key={}

            try:
                shehui_xinyong = driver.find_element(
                    By.XPATH,
                    '//*[@id="cominfo"]/div[2]/table/tr[1]/td[2]/div/span[1]'
                    #     xpath: '//*[@id="cominfo"]/div[2]/table/tr[1]/td[2]/div/span[1]
                ).text
                print("shehui_xinyong:", shehui_xinyong)
            except:
                shehui_xinyong = ""

            try:
                zhuceziben = driver.find_element(
                    By.XPATH,
                    '//*[@id="cominfo"]/div[2]/table/tr[3]/td[2]'
                    #    xpath: //*[@id="cominfo"]/div[2]/table/tr[3]/td[2]
                ).text
                print("zhuceziben:", zhuceziben)

            except:
                zhuceziben = ""

            try:
                fadingdaibiaoren = driver.find_element(
                    By.XPATH,
                    '//*[@id="cominfo"]/div[2]/table/tr[2]/td[2]/div/div/span[2]/span/span/a'
                    #     xpath://*[@id="cominfo"]/div[2]/table/tr[2]/td[2]/div/div/span[2]/span/span/a
                ).text
                print("fadingdaibiaoren:", fadingdaibiaoren)

            except:
                fadingdaibiaoren = ""

            try:
                suoshuhangye = driver.find_element(
                    By.XPATH, '//*[@id="cominfo"]/div[2]/table/tr[8]/td[2]/ul'
                ).text
            except:
                suoshuhangye = ""

            try:
                jingyingfanwei = driver.find_element(
                    By.XPATH,
                    '//*[@id="cominfo"]/div[2]/table/tr[10]/td[2]/div/span[1]'
                    #     xpath://*[@id="cominfo"]/div[2]/table/tr[10]/td[2]/div/span[1]
                ).text
            except:
                jingyingfanwei = ""

            try:
                zhucedizhi = driver.find_element(
                    By.XPATH,
                    '//*[@id="cominfo"]/div[2]/table/tr[9]/td[2]/div/span[1]/a[1]'
                    #     xpath://*[@id="cominfo"]/div[2]/table/tr[9]/td[2]/div/span[1]/a[1]
                ).text
            except:
                zhucedizhi = ""

            try:
                qiyeguimo = driver.find_element(
                    By.XPATH,
                    "/html/body/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/span[2]/span",
                ).text
            except:
                qiyeguimo = ""

        except WebDriverException:
            shehui_xinyong = zhuceziben = fadingdaibiaoren = suoshuhangye = jingyingfanwei = zhucedizhi = qiyeguimo = ""

        msg_dict = {
            "统一社会信用代码": shehui_xinyong,
            "注册资本": zhuceziben,
            "法定代表人/负责人": fadingdaibiaoren,
            "所属行业": suoshuhangye,
            "经营范围": jingyingfanwei,
            "注册地址": zhucedizhi,
            "企业规模": qiyeguimo,  # 企业规模 是 企查查中的公司别名
        }

        for name in msg_dict:
            if msg_dict[name]:
                msg_dict[name] = str(msg_dict[name]).replace(" ", "").replace("\n", "")
        print("msg_dict:", msg_dict)

        for name in check_dict:
            before = str(row[name]).strip()
            new = msg_dict[name]
            # 判断新旧内容是否有变化
            if before == new:
                check_dict[name].append(before)
            elif not new:
                check_dict[name].append(before)
            else:
                check_dict[name].append(new)

    for name in check_dict:
        data[name] = check_dict[name]
    data.to_excel(path, index=None)


if __name__ == "__main__":
    get_company_url()  # 通过公司名字获取url，开始登录需要验证码，需要手动输入
    get_company_msg()  # 通过公司url获取对应字段，开始登录需要验证码，需要手动输入
