import os
import pandas as pd
import re

degree_mapping = {
    '学士': 0,
    '硕士': 1,
    '博士': 2,
    '其他': 3
}

degree = '博士'

degree_value = degree_mapping.get(degree, -1)
print(f'学历为{degree_value}')