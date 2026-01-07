import math
import re

def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD09)转火星坐标系(GCJ02)
    参数: bd_lon:百度经度, bd_lat:百度纬度
    返回: (gcj_lon, gcj_lat)
    """
    x_pi = math.pi * 3000.0 / 180.0
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gcj_lon = z * math.cos(theta)
    gcj_lat = z * math.sin(theta)
    return gcj_lon, gcj_lat

def convert_coordinates(file_path, output_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配坐标点并进行转换
    pattern = r'({ lng: ([\d.]+),\s*lat: ([\d.]+) })'
    
    def replace_coord(match):
        full_str = match.group(1)
        lng = float(match.group(2))
        lat = float(match.group(3))
        new_lng, new_lat = bd09_to_gcj02(lng, lat)
        return f'{{ lng: {new_lng:.6f}, lat: {new_lat:.6f} }}'
    
    # 替换所有坐标点
    new_content = re.sub(pattern, replace_coord, content)
    
    # 写入新文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

# 使用示例
convert_coordinates('D:\project\百度坐标.txt', 'D:\project\高德坐标.txt')
