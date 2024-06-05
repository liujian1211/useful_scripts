import os
import pandas as pd
import re

name = '葛  为**'

name = name.replace('*', '') #去掉名字中的*
if re.search('[\u4e00-\u9fa5]', name):
    name = re.sub(r'\s+', '', name)

print(f'名字为{name}')