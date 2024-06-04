import re
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    # path = "test.xlsx"
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
    url = ("https://rc.czrc.com.cn/rcm/#/login" )
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
            name_blank = driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/header/div/div/form/span[1]/form/div[1]/div[2]/div/div/div/input")
            name_blank.clear()
            name_blank.send_keys(clean_name)
            # driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/header/div/div/form/span[1]/form/div[1]/div[2]/div/div/div/input").clear().send_keys(clean_name)
            time.sleep(2)

            #点击筛选
            driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/header/div/div/form/span[2]/button").click()

            #获取”筛选“完之后的表格
            table = driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/main/div/div[3]/table/tbody")
            time.sleep(1)
            rows = table.find_elements(By.XPATH, './/tr[position()>=1]')

            # 计算有内容的行数
            # non_empty_rows = [row for row in rows if row.text.strip() != '']
            # row_count = len(non_empty_rows)

            count=0
            for _row in rows:
                try:
                    if _row.text!="":
                        count+=1
                        time.sleep(1)
                except:
                    time.sleep(1)
                    continue
            print(f'{clean_name}的count为', count)
            # print(f'{clean_name}的row_count为',row_count)

            #若表格只有1行
            if count==1:

                #点击“查看”按钮
                driver.find_element(By.XPATH,"//*[@id='app']/div/div[3]/section/div/section/main/div/div[5]/div[2]/table/tbody/tr/td[11]/div/span/a[1]/span").click()

                #等待v-modal类型的元素出现
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'v-modal')))

                #等待el-dialog__wrapper edialog类型的元素出现
                dialog = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dialog__wrapper')))

                # 等待el-dialog__header元素出现
                dialog_header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dialog__header')))

                iframes = driver.find_elements(By.TAG_NAME, "iframe")

                # for iframe in iframes:print(iframe.get_attribute("src"))  # 输出iframe的src属性以确认

                driver.get(iframes[0].get_attribute("src"))
                iframe = driver.find_element(By.ID,"lr_iframe_")
                driver.switch_to.frame(iframe)  #进入到新的子页面

                time.sleep(1)

                try:
                    birthdate_element = driver.find_element(By.ID,"3706e5fc-4eb0-ba4a-e4b7-d4bdf9537a31")
                    time.sleep(1)
                    birthdate = birthdate_element.get_attribute("value")
                    print(f"{clean_name}的生日:", birthdate)
                except Exception as e:
                    print(f'没找到{clean_name}的生日信息')

                try:
                    degree_element = driver.find_element(By.XPATH,"//*[@id='42e5fc73-2a69-83c5-9ff3-027fdcc36ec5']/div")
                    time.sleep(1)
                    degree = degree_element.text
                    degree_value = degree_mapping.get(degree, -1)
                    print(f"{clean_name}的学位：", degree_value)
                except Exception as e:
                    print(f'没找到{clean_name}的学位信息')

                try:
                    document_type_element = driver.find_element(By.XPATH,"//*[@id='19643e11-1ab4-e944-166f-e0f910c677eb']")
                    time.sleep(1)
                    document_type = document_type_element.text
                    print(f'{clean_name}的证件类型：',document_type)
                    document_value = document_mapping.get(document_type, -1)
                except Exception as e:
                    print(f'没找到{clean_name}的证件类型')

                try:
                    document_num_element = driver.find_element(By.ID,"2132f671-ee86-6897-d92d-825776af523b")
                    time.sleep(1)
                    document_num = document_num_element.get_attribute("value")
                    print(f'{clean_name}的证件号码：', document_num)
                except Exception as e:
                    print(f'没找到{clean_name}的证件号码')

                try:
                    cell_num_element = driver.find_element(By.ID,"451e263b-6791-9025-eced-34b41c802f91")
                    time.sleep(1)
                    cell_num = cell_num_element.get_attribute("value")
                    print(f'{clean_name}的联系方式：', cell_num)
                except Exception as e:
                    print(f'没找到{clean_name}的联系方式')

                try:
                    #点击“创业项目”
                    driver.find_element(By.XPATH,"//*[@id='lr_form_tabs_box']/ul/li[2]/a").click()
                    project_name_element = driver.find_element(By.ID,"f63b9b26-8fc0-02f9-5e94-44c758e82744")
                    time.sleep(1)
                    project_name = project_name_element.get_attribute("value")
                    print(f'{clean_name}的创业项目名称：{project_name}\n')
                except Exception as e:
                    print(f'{clean_name}的创业项目点击失败')

                data.at[index, '出生日期'] = birthdate
                data.at[index,'学位选择'] = degree_value
                data.at[index,'证件类型'] = document_value
                data.at[index,'证件号码'] = document_num
                data.at[index,'人才联系方式'] = cell_num
                data.at[index,'项目名称'] = project_name
                data.to_excel("updated.xlsx",index=False)

                # 退出子页面，回到原来的页面
                driver.get(url)
                time.sleep(1)

            elif count>=2:  #多行表示有重名的人才，此时比较批次
                for index_, row_ in enumerate(rows):
                    columns = row_.find_elements(By.XPATH, './/td')
                    batch_ = columns[2].text

                    if extract_between_first_and_batch2(batch_)==batch_num:  #只有人才姓名和批次号都一样才会进入判断
                        search_xpath = f"//*[@id='app']/div/div[3]/section/div/section/main/div/div[5]/div[2]/table/tbody/tr[{index_+1}]/td[11]/div/span/a[1]/span"
                        driver.find_element(By.XPATH,search_xpath).click()

                        # 等待v-modal类型的元素出现
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'v-modal')))

                        # 等待el-dialog__wrapper edialog类型的元素出现
                        dialog = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dialog__wrapper')))

                        # 等待el-dialog__header元素出现
                        dialog_header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dialog__header')))

                        iframes = driver.find_elements(By.TAG_NAME, "iframe")

                        driver.get(iframes[0].get_attribute("src"))
                        iframe = driver.find_element(By.ID, "lr_iframe_")
                        driver.switch_to.frame(iframe)  # 进入到新的子页面

                        time.sleep(1)

                        try:
                            birthdate_element = driver.find_element(By.ID, "3706e5fc-4eb0-ba4a-e4b7-d4bdf9537a31")
                            time.sleep(1)
                            birthdate = birthdate_element.get_attribute("value")
                            print(f"{clean_name}的生日:", birthdate)
                        except Exception as e:
                            print(f'没找到{clean_name}的生日信息')

                        try:
                            degree_element = driver.find_element(By.XPATH,"//*[@id='42e5fc73-2a69-83c5-9ff3-027fdcc36ec5']/div")
                            time.sleep(1)
                            degree = degree_element.text
                            degree_value = degree_mapping.get(degree, -1)
                            print(f"{clean_name}的学位：", degree_value)
                        except Exception as e:
                            print(f'没找到{clean_name}的学位信息')

                        try:
                            document_type_element = driver.find_element(By.XPATH,"//*[@id='19643e11-1ab4-e944-166f-e0f910c677eb']")
                            time.sleep(1)
                            document_type = document_type_element.text
                            print(f'{clean_name}的证件类型：', document_type)
                            document_value = document_mapping.get(document_type, -1)
                        except Exception as e:
                            print(f'没找到{clean_name}的证件类型')

                        try:
                            document_num_element = driver.find_element(By.ID, "2132f671-ee86-6897-d92d-825776af523b")
                            time.sleep(1)
                            document_num = document_num_element.get_attribute("value")
                            print(f'{clean_name}的证件号码：', document_num)
                        except Exception as e:
                            print(f'没找到{clean_name}的证件号码')

                        try:
                            cell_num_element = driver.find_element(By.ID, "451e263b-6791-9025-eced-34b41c802f91")
                            time.sleep(1)
                            cell_num = cell_num_element.get_attribute("value")
                            print(f'{clean_name}的联系方式：', cell_num)
                        except Exception as e:
                            print(f'没找到{clean_name}的联系方式\n')

                        try:
                            # 点击“创业项目”
                            driver.find_element(By.XPATH, "//*[@id='lr_form_tabs_box']/ul/li[2]/a").click()
                            project_name_element = driver.find_element(By.ID, "f63b9b26-8fc0-02f9-5e94-44c758e82744")
                            time.sleep(1)
                            project_name = project_name_element.get_attribute("value")
                            print(f'{clean_name}的创业项目名称：', project_name)
                        except Exception as e:
                            print(f'{clean_name}的创业项目点击失败')

                        data.at[index, '出生日期'] = birthdate
                        data.at[index, '学位选择'] = degree_value
                        data.at[index, '证件类型'] = document_value
                        data.at[index, '证件号码'] = document_num
                        data.at[index, '人才联系方式'] = cell_num
                        data.at[index, '项目名称'] = project_name
                        data.to_excel("updated.xlsx", index=False)

                        # 退出子页面，回到原来的页面
                        driver.get(url)
                        time.sleep(1)
                        break  #退出内部循环

            else:  #若系统中查无此人
                print(f'系统中查不到{clean_name}')
                time.sleep(1)
                continue

if __name__ == "__main__":
    get_company_url()
