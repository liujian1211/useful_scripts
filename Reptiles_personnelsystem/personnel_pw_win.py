import re
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By

credit_code = []
registered_capital = []
juridical_person = []
personnel = []
industry = []
business_scope = []
registered_address = []
enterprise_scale = []

check_dict = {
    "统一社会信用代码": credit_code,
    "注册资本": registered_capital,
    "法定代表人/负责人": juridical_person,
    "人才姓名": personnel,
}

#徐某的账号密码
username = "wjq"
password = "wjrc666666_AA00q!!"

#获取表格中的人才的批次
def extract_between_first_and_batch(text):
    pattern = r'第(.*?)批'
    result = re.search(pattern, text)

    if result:
        return result.group(1)
    else:
        return None

def extract_between_first_and_batch2(text):
    pattern = r'才(.*?)批'
    result = re.search(pattern, text)

    if result:
        return result.group(1)
    else:
        return None

degree_mapping = {
    '学士': 0,
    '硕士': 1,
    '博士': 2,
    '其他': 3
}

document_mapping = {
    '身份证':0,
    '护照':1,
    '军官证':2,
    '港澳居民来往内地通行证':3,
    '台湾居民来往大陆通行证':4
}

def get_company_url():
    path = "西太湖_人才企业信息统计.xlsx"
    data = pd.read_excel(path, sheet_name=1)  # 读取第2个sheet的全部数据,int整数用于引用的sheet的索引（从0开始）

    option = webdriver.ChromeOptions()
    option.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )  # webdriver防检测

    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-usage")
    driver = webdriver.Chrome(options=option)

    driver.set_page_load_timeout(25)
    driver.delete_all_cookies()
    url = ("https://rc.czrc.com.cn/rcm/#/login" )  # "https://www.qcc.com/weblogin?back=%2F"
    driver.get(url)
    time.sleep(1)

    # 输入账号密码
    driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[1]/div[4]/div/div/form/div[2]/div/div/input").send_keys(username)
    driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[1]/div[4]/div/div/form/div[3]/div/div/input").send_keys(password)
    time.sleep(8)  # 8秒内输完验证码
    driver.find_element(By.XPATH,"//*[@id='app']/div/div/div[1]/div[4]/div/div/form/button").click()
    time.sleep(3)

    # 点击“19及之前历史数据查询”
    url = ("https://rc.czrc.com.cn/rcm/#/rcmside/rcmxsqold/rcmxsqold")  #“19及之前历史数据查询”的url

    driver.get(url)
    time.sleep(2)
    print("进入到'19及之前历史数据查询'")

    #遍历人才表里的每一个人才
    for index, row in data.iterrows():
        name = row["姓名"]
        batch = row["入选批次"]

        if pd.notnull(name):
            clean_name = name.replace('*', '')  #获取该行的人才姓名
            batch_num = extract_between_first_and_batch(batch)  #获取该行的人才批次

            #填入姓名
            driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/header/div/div/form/span[1]/form/div[1]/div[2]/div/div/div/input").send_keys(clean_name)
            time.sleep(2)

            #点击筛选
            driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/header/div/div/form/span[2]/button").click()

            #获取”筛选“完之后的表格
            table = driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/main/div/div[3]/table/tbody")
            rows = table.find_elements(By.XPATH, './/tr[position() >= 1]')
            # rows = table.find_elements(By.TAG_NAME, 'tr')

            count=0
            for _row in rows:
                try:
                    if _row.text!="":
                        count+=1
                        time.sleep(1)
                except:
                    continue

            #若表格只有1行
            if(count==1):
                #点击“查看”按钮
                driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/main/div/div[5]/div[2]/table/tbody/tr/td[11]/div/span/a[1]/span").click()
                time.sleep(5)  #等5s加载完成

                try:
                    birthDay = driver.find_element(By.ID,"3706e5fc-4eb0-ba4a-e4b7-d4bdf9537a31")
                    time.sleep(3)
                except NoSuchElementException:
                    print('没找到生日信息')
                # birthDay_value = birthDay.get_attribute("value")
                # print(f'生日的值为{birthDay_value}')
                degree = driver.find_element(By.XPATH,"//*[@id='42e5fc73-2a69-83c5-9ff3-027fdcc36ec5']/div").text
                degree_value = degree_mapping.get(degree, -1)
                document_type = driver.find_element(By.XPATH,"//*[@id='19643e11-1ab4-e944-166f-e0f910c677eb']").text
                document_value = document_mapping.get(document_type,-1)
                document_num = driver.find_element(By.XPATH,"//*[@id='2132f671-ee86-6897-d92d-825776af523b']").text
                cell_num = driver.find_element(By.XPATH,"//*[@id='451e263b-6791-9025-eced-34b41c802f91']").text

                # data.at[index, '出生日期'] = birthDay_value
                data.at[index,'学位选择'] = degree_value
                data.at[index,'证件类型'] = document_value
                data.at[index,'证件号码'] = document_num
                data.at[index,'人才联系方式'] = cell_num
                data.to_excel(path,index=False)
            else:  #多行表示有重名的人才，此时比较批次
                for row_index, row_ in rows:
                    columns = row_.find_elements(By.XPATH, './/td')
                    batch_ = columns[2].text
                    #若表格有多行，则判断后更改tr后的数字
                    if extract_between_first_and_batch2(batch_)==batch_num:  #只有人才姓名和批次号都一样才会进入判断
                        driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/main/div/div[3]/table/tbody/tr[index]/td[11]/div/span/a[1]/span")
                        time.sleep(5)  # 等5s加载完成

                        birthDay = driver.find_element(By.XPATH, "//*[@id='3706e5fc-4eb0-ba4a-e4b7-d4bdf9537a31']").text
                        degree = driver.find_element(By.XPATH,"//*[@id='42e5fc73-2a69-83c5-9ff3-027fdcc36ec5']/div").text
                        degree_value = degree_mapping.get(degree, -1)
                        document_type = driver.find_element(By.XPATH,"//*[@id='19643e11-1ab4-e944-166f-e0f910c677eb']").text
                        document_value = document_mapping.get(document_type, -1)
                        document_num = driver.find_element(By.XPATH,"//*[@id='2132f671-ee86-6897-d92d-825776af523b']").text
                        cell_num = driver.find_element(By.XPATH, "//*[@id='451e263b-6791-9025-eced-34b41c802f91']").text

                        data.at[index, '出生日期'] = birthDay
                        data.at[index, '学位选择'] = degree_value
                        data.at[index, '证件类型'] = document_value
                        data.at[index, '证件号码'] = document_num
                        data.at[index, '人才联系方式'] = cell_num
                        data.to_excel(path, index=False)

                    else:
                        continue


if __name__ == "__main__":
    get_company_url()
