import math
from typing import List, Tuple


class CameraParams:
    """相机参数"""
    # 100m 高度时的覆盖范围
    coverage_width_100m: float = 161.19   # 宽度（米）
    coverage_height_100m: float = 106.67  # 高度（米）
    
    # 重叠率（可配置，默认为 0，即无重叠）
    side_overlap: float = 0.0     # 侧向重叠率（0-1）
    forward_overlap: float = 0.0  # 前向重叠率（0-1）


class FlightPlanner:
    """航线规划器"""
    
    def __init__(self, height: float = 100.0):
        """
        初始化航线规划器
        
        Args:
            height: 飞行高度（米）
        """
        self.height = height
        self.camera = CameraParams
        self._calculate_parameters()
    
    def _calculate_parameters(self):
        """根据高度计算各项参数"""
        # 计算缩放比例（线性关系）
        scale = self.height / 100.0
        
        # 单张照片覆盖范围（按高度线性缩放）
        self.coverage_width = self.camera.coverage_width_100m * scale
        self.coverage_height = self.camera.coverage_height_100m * scale
        
        # 航线间距
        self.line_spacing = self.coverage_width * (1 - self.camera.side_overlap)
        
        # 航点间距
        self.point_spacing = self.coverage_height * (1 - self.camera.forward_overlap)
    
    def geo_to_xy(self, lon: float, lat: float, ref_lon: float = None, ref_lat: float = None) -> Tuple[float, float]:
        """
        将经纬度转换为平面坐标（米）
        
        Args:
            lon: 经度
            lat: 纬度
            ref_lon: 参考经度（原点）
            ref_lat: 参考纬度（原点）
        
        Returns:
            (x, y) 米坐标
        """
        if ref_lon is None or ref_lat is None:
            ref_lon, ref_lat = lon, lat
        
        # 使用墨卡托近似投影
        # 1 度纬度 ≈ 111320 米
        # 1 度经度 ≈ 111320 * cos(纬度) 米
        lat_rad = math.radians(ref_lat)
        
        x = (lon - ref_lon) * 111320 * math.cos(lat_rad)
        y = (lat - ref_lat) * 111320
        
        return x, y
    
    def xy_to_geo(self, x: float, y: float, ref_lon: float, ref_lat: float) -> Tuple[float, float]:
        """
        将平面坐标转换回经纬度
        
        Args:
            x: 米坐标
            y: 米坐标
            ref_lon: 参考经度（原点）
            ref_lat: 参考纬度（原点）
        
        Returns:
            (lon, lat) 经纬度
        """
        lat_rad = math.radians(ref_lat)
        
        lon = ref_lon + x / (111320 * math.cos(lat_rad))
        lat = ref_lat + y / 111320
        
        return lon, lat
    
    def get_polygon_vertices(self, boundary_points: List[Tuple[float, float]]) -> Tuple[List[float], List[float]]:
        """
        获取多边形的顶点坐标（平面坐标）
        
        Args:
            boundary_points: 经纬度边界点列表 [(lon1, lat1), (lon2, lat2), ...]
        
        Returns:
            (xs, ys) 平面坐标列表
        """
        # 使用第一个点作为参考原点
        ref_lon, ref_lat = boundary_points[0]
        
        xs, ys = [], []
        for lon, lat in boundary_points:
            x, y = self.geo_to_xy(lon, lat, ref_lon, ref_lat)
            xs.append(x)
            ys.append(y)
        
        return xs, ys, ref_lon, ref_lat
    
    def get_bounding_box(self, xs: List[float], ys: List[float]) -> Tuple[float, float, float, float]:
        """
        获取边界框
        
        Returns:
            (min_x, max_x, min_y, max_y)
        """
        return min(xs), max(xs), min(ys), max(ys)
    
    def point_in_polygon(self, x: float, y: float, xs: List[float], ys: List[float]) -> bool:
        """
        判断点是否在多边形内（射线法）
        """
        n = len(xs)
        inside = False
        
        j = n - 1
        for i in range(n):
            if ((ys[i] > y) != (ys[j] > y)) and (x < (xs[j] - xs[i]) * (y - ys[i]) / (ys[j] - ys[i]) + xs[i]):
                inside = not inside
            j = i
        
        return inside
    
    
    def generate_flight_lines(self, boundary_points: List[Tuple[float, float]]) -> List[List[Tuple[float, float]]]:
        """
        生成航线线段
        
        Args:
            boundary_points: 经纬度边界点列表
        
        Returns:
            航线列表，每条航线包含多个点
        """
        # 转换为平面坐标
        xs, ys, ref_lon, ref_lat = self.get_polygon_vertices(boundary_points)
        
        # 获取边界框
        min_x, max_x, min_y, max_y = self.get_bounding_box(xs, ys)
        
        # 计算覆盖范围（用于边界判断）
        # 航点位置需要确保其覆盖范围能完全覆盖目标区域
        half_width = self.coverage_width / 2
        half_height = self.coverage_height / 2
        
        # 生成航线
        flight_lines = []
        
        # 计算航线数量
        # 从边界框开始，确保覆盖整个区域
        num_lines = int((max_x - min_x) / self.line_spacing) + 2
        
        for i in range(num_lines):
            # 航线的 x 坐标
            line_x = min_x + i * self.line_spacing
            
            # 收集该航线上的点
            line_points = []
            
            # 计算航线的 y 范围
            num_points = int((max_y - min_y) / self.point_spacing) + 2
            
            for j in range(num_points):
                point_y = min_y + j * self.point_spacing
                
                # 检查该航点的覆盖范围是否与目标区域有交集
                # 航点覆盖范围：[point_x - half_width, point_x + half_width] x [point_y - half_height, point_y + half_height]
                # 检查这个矩形是否与多边形有交集
                if self._coverage_intersects_polygon(line_x, point_y, half_width, half_height, xs, ys):
                    line_points.append((line_x, point_y))
            
            if len(line_points) >= 1:
                flight_lines.append(line_points)
        
        return flight_lines, ref_lon, ref_lat
    
    def _coverage_intersects_polygon(self, cx: float, cy: float, half_w: float, half_h: float, 
                                      xs: List[float], ys: List[float]) -> bool:
        """
        检查以 (cx, cy) 为中心，宽度 2*half_w，高度 2*half_h 的矩形是否与多边形有交集
        
        Args:
            cx, cy: 矩形中心
            half_w, half_h: 矩形半宽和半高
            xs, ys: 多边形顶点
        
        Returns:
            是否有交集
        """
        # 检查 1：矩形中心是否在多边形内
        if self.point_in_polygon(cx, cy, xs, ys):
            return True
        
        # 检查 2：矩形的四个角点是否在多边形内
        corners = [
            (cx - half_w, cy - half_h),
            (cx + half_w, cy - half_h),
            (cx + half_w, cy + half_h),
            (cx - half_w, cy + half_h)
        ]
        
        for corner_x, corner_y in corners:
            if self.point_in_polygon(corner_x, corner_y, xs, ys):
                return True
        
        # 检查 3：多边形的任何边是否与矩形相交
        n = len(xs)
        for i in range(n):
            j = (i + 1) % n
            if self._line_intersects_rect(xs[i], ys[i], xs[j], ys[j], 
                                          cx - half_w, cy - half_h, 
                                          cx + half_w, cy + half_h):
                return True
        
        return False
    
    def _line_intersects_rect(self, x1: float, y1: float, x2: float, y2: float,
                               rx_min: float, ry_min: float, rx_max: float, ry_max: float) -> bool:
        """检查线段是否与矩形相交"""
        # 使用 Cohen-Sutherland 算法的简化版本
        # 检查线段两端点是否都在矩形外且在同侧
        def compute_outcode(x, y):
            code = 0
            if x < rx_min:
                code |= 1
            elif x > rx_max:
                code |= 2
            if y < ry_min:
                code |= 4
            elif y > ry_max:
                code |= 8
            return code
        
        outcode1 = compute_outcode(x1, y1)
        outcode2 = compute_outcode(x2, y2)
        
        # 如果两端点都在矩形同一侧外部，则不相交
        if (outcode1 & outcode2) != 0:
            return False
        
        # 如果任一端点在矩形内，则相交
        if outcode1 == 0 or outcode2 == 0:
            return True
        
        # 使用参数方程检查线段是否与矩形边相交
        dx = x2 - x1
        dy = y2 - y1
        
        if abs(dx) < 1e-10:
            # 垂直线
            if x1 < rx_min or x1 > rx_max:
                return False
            t_min = max(0, (ry_min - y1) / dy) if dy > 0 else (ry_max - y1) / dy
            t_max = min(1, (ry_max - y1) / dy) if dy > 0 else (ry_min - y1) / dy
            return t_min <= t_max and t_max >= 0 and t_min <= 1
        elif abs(dy) < 1e-10:
            # 水平线
            if y1 < ry_min or y1 > ry_max:
                return False
            t_min = max(0, (rx_min - x1) / dx) if dx > 0 else (rx_max - x1) / dx
            t_max = min(1, (rx_max - x1) / dx) if dx > 0 else (rx_min - x1) / dx
            return t_min <= t_max and t_max >= 0 and t_min <= 1
        else:
            # 一般情况：检查与四条边的交点
            t_min = 0
            t_max = 1
            
            # 检查 x 范围
            t1 = (rx_min - x1) / dx
            t2 = (rx_max - x1) / dx
            if t1 > t2:
                t1, t2 = t2, t1
            t_min = max(t_min, t1)
            t_max = min(t_max, t2)
            
            if t_min > t_max:
                return False
            
            # 检查 y 范围
            t1 = (ry_min - y1) / dy
            t2 = (ry_max - y1) / dy
            if t1 > t2:
                t1, t2 = t2, t1
            t_min = max(t_min, t1)
            t_max = min(t_max, t2)
            
            return t_min <= t_max and t_max >= 0 and t_min <= 1
    
    def optimize_flight_lines(self, flight_lines: List[List[Tuple[float, float]]]) -> List[List[Tuple[float, float]]]:
        """
        优化航线顺序，形成连续的"弓"形路径
        
        Args:
            flight_lines: 原始航线列表
        
        Returns:
            优化后的航线列表
        """
        if not flight_lines:
            return []
        
        # 交替方向，形成弓形
        optimized = []
        for i, line in enumerate(flight_lines):
            if i % 2 == 0:
                optimized.append(line)
            else:
                optimized.append(line[::-1])  # 反转
        
        return optimized
    
    def generate_flight_points(self, boundary_points: List[Tuple[float, float]], 
                               altitude: float) -> List[dict]:
        """
        生成完整的航线点列表
        
        Args:
            boundary_points: 经纬度边界点列表 [(lon1, lat1), ...]
            altitude: 飞行高度（米）
        
        Returns:
            航线点列表
        """
        self.height = altitude
        self._calculate_parameters()
        
        # 生成航线
        flight_lines, ref_lon, ref_lat = self.generate_flight_lines(boundary_points)
        
        if not flight_lines:
            print("警告：未生成任何航线，请检查边界点和高度参数")
            return []
        
        # 优化航线顺序
        optimized_lines = self.optimize_flight_lines(flight_lines)
        
        # 转换为经纬度并生成航点
        flight_points = []
        point_id = 1
        
        for line_idx, line in enumerate(optimized_lines):
            for point_idx, (x, y) in enumerate(line):
                lon, lat = self.xy_to_geo(x, y, ref_lon, ref_lat)
                
                flight_points.append({
                    'id': point_id,
                    'line': line_idx + 1,
                    'point_in_line': point_idx + 1,
                    'longitude': round(lon, 8),
                    'latitude': round(lat, 8),
                    'altitude': altitude,
                    'heading': 0.0,  # 默认航向角
                    'gimbal_pitch': -90.0  # 云台俯仰角（垂直向下）
                })
                point_id += 1
        
        # 统计信息
        total_distance = self._calculate_total_distance(flight_points)
        self._total_distance = total_distance  # 保存供外部访问
        
        print(f"\n总航程：{total_distance:.2f} m")
        print()
        
        return flight_points
    
    def _calculate_total_distance(self, points: List[dict]) -> float:
        """计算总航程"""
        if len(points) < 2:
            return 0.0
        
        total = 0.0
        # 使用第一个点作为参考点
        ref_lon = points[0]['longitude']
        ref_lat = points[0]['latitude']
        
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            
            # 使用平面坐标近似计算距离
            x1, y1 = self.geo_to_xy(p1['longitude'], p1['latitude'], ref_lon, ref_lat)
            x2, y2 = self.geo_to_xy(p2['longitude'], p2['latitude'], ref_lon, ref_lat)
            
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total += dist
        
        return total


if __name__ == "__main__":
    # 配置区域边界点（经纬度坐标）
    BOUNDARY_POINTS = [
        (119.48034172, 31.66011228),  
        (119.48059198, 31.65924308),   
        (119.48154204, 31.65943758),   
        (119.48128946, 31.66033012),   
    ]
    
    # 飞行高度（米）
    FLIGHT_HEIGHT = 100.0
    
    # 创建航线规划器并生成航线
    planner = FlightPlanner(height=FLIGHT_HEIGHT)
    flight_points = planner.generate_flight_points(BOUNDARY_POINTS, FLIGHT_HEIGHT)
    
    if flight_points:
        # 输出所有航点
        print("航线点:")
        for point in flight_points:
            print(f"  {point['longitude']:.8f}, {point['latitude']:.8f}, {point['altitude']}m")
        
        # 计算并输出总航程
        total_distance = planner._calculate_total_distance(flight_points)
        print(f"\n总航程：{total_distance:.2f} m")