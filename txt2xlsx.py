import pandas as pd
import json

with open('D:/AkyPower/20240628_203707.txt', 'r') as file:
    data = file.readlines()

def extract_values(entry):
    # dev_type = entry['dev_type']
    inverter = entry['inverter']
    date_time = entry['time']
    date,time = date_time.split(' ')
    AH = inverter['AH']
    AT = inverter['AT']
    DPT = inverter['DPT']
    GHI = inverter['GHI']
    GTI = inverter['GTI']
    MT = inverter['MT']
    MaxT = inverter['MaxT']
    MinT = inverter['MinT']
    ac_gen_day = inverter['ac_gen_day']
    ac_gen_total = inverter['ac_gen_total']
    efficy = inverter['efficy']
    freq = inverter['freq']
    ia = inverter['ia']
    ib = inverter['ib']
    ic = inverter['ic']
    model = inverter['model']
    pac = inverter['pac']
    pf = inverter['pf']
    preac = inverter['preac']
    sn = inverter['sn']
    temp = inverter['temp']
    ua = inverter['ua']
    ub = inverter['ub']
    uc = inverter['uc']

    return {
            'date':date,
            'time':time,
            # 'date_time':date_time,
            'AH':AH,
            'AT':AT,
            'DPT':DPT,
            'GHI':GHI,
            'GTI':GTI,
            'MT' : MT,
            'MaxT' :MaxT,
            'MinT':MinT,
            'ac_gen_day':ac_gen_day,
            'ac_gen_total': ac_gen_total,
            'efficy' : efficy,
            'frep': freq,
            'ia': ia,
            'ib':ib,
            'ic':ic,
            'model' :model,
            'pac':pac,
            'pf':pf,
            'preac':preac,
            'sn':sn,
            'temp':temp,
            'ua':ua,
            'ub':ub,
            'uc':uc
    }

parsed_data = [extract_values(json.loads(line)) for line in data]

# 将数据写入Excel文件
df = pd.DataFrame(parsed_data)

# 如果想要将数据写入一个新的excel文件，使用下面的代码
df.to_excel('D:/AkyPower/20240628_0710.xlsx', index=False)

print('写入完成')