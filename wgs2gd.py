import math

def wgs84_to_gcj02(lng, lat):
    """
    将WGS-84坐标转换为GCJ-02坐标（高德地图坐标系）
    参数: lng (float) - 经度, lat (float) - 纬度
    返回: [经度, 纬度]
    """
    # 检查是否在国内范围（中国境内）
    if not (73.66 <= lng <= 135.05 and 3.86 <= lat <= 53.55):
        return [lng, lat]
    
    a = 6378245.0  # 长半轴
    ee = 0.00669342162296594323  # 偏心率平方
    
    # 转换函数
    def transform_lng(x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return ret
    
    def transform_lat(x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret
    
    # 计算偏移量
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    
    # 返回转换后的坐标
    return [lng + dlng, lat + dlat]

# 原始坐标（WGS-84）
lng = 119.474784519
lat = 31.663955677

# 转换为高德坐标（GCJ-02）
gcj02_coord = wgs84_to_gcj02(lng, lat)

print(f"原始坐标 (WGS-84): [{lng}, {lat}]")
print(f"高德坐标 (GCJ-02): {gcj02_coord}")