import pandas as pd

path = "qichacha_csdn/company_msg.xlsx"
data = pd.read_excel(path, sheet_name=0)

url = [i for i in range(1, 17)]


# data["url"] = url

for index, row in data.iterrows():
    data.at[index, 'url'] = url[index]
    data.to_excel("qichacha_csdn/updated3.xlsx", index=False)