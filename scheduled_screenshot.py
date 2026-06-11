"""
Windows定时截屏脚本
功能：按照设定的时间间隔自动截取屏幕并保存为图片
支持单显示器和多显示器环境
"""
import time
import os
from datetime import datetime
from PIL import ImageGrab


def get_monitor_info():
    """
    获取显示器信息
    
    Returns:
        显示器数量和信息列表
    """
    try:
        # 尝试获取所有显示器的边界框
        monitors = ImageGrab.grab().getbbox()
        return 1, [monitors]
    except:
        return 1, [None]


def take_screenshot(save_dir="screenshots", monitor_index=None):
    """
    截取当前屏幕并保存到指定目录
    
    Args:
        save_dir: 保存图片的目录名称
        monitor_index: 显示器索引，None表示主显示器，0=主显示器，1=第二显示器，以此类推
        
    Returns:
        保存的文件路径
    """
    # 创建保存目录（如果不存在）
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成文件名（使用时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 精确到毫秒
    
    # 根据显示器索引生成不同的文件名前缀
    if monitor_index is None:
        prefix = "screenshot"
    else:
        prefix = f"screenshot_monitor{monitor_index}"
    
    filename = f"{prefix}_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    
    # 截取屏幕
    try:
        if monitor_index is not None:
            # 截取指定显示器
            # 注意：Pillow的ImageGrab在Windows上可以通过bbox参数指定区域
            # 这里使用all_screens=True来获取所有屏幕的信息
            screenshot = ImageGrab.grab(all_screens=True)
            
            # 如果需要截取特定显示器，需要使用其他方法
            # 这里先截取全屏，然后可以根据需要裁剪
            screenshot.save(filepath, "PNG")
        else:
            # 截取主屏幕
            screenshot = ImageGrab.grab()
            screenshot.save(filepath, "PNG")
    except Exception as e:
        print(f"截图失败: {e}")
        # 降级方案：截取整个桌面（包括所有显示器）
        screenshot = ImageGrab.grab(all_screens=True)
        screenshot.save(filepath, "PNG")
    
    return filepath


def take_screenshot_with_pyscreenshot(save_dir="screenshots", monitor_index=1):
    """
    使用mss库截取指定显示器（推荐用于多显示器环境）
    
    Args:
        save_dir: 保存图片的目录名称
        monitor_index: 显示器索引，1=第一显示器，2=第二显示器，以此类推
        
    Returns:
        保存的文件路径
    """
    try:
        import mss
        import mss.tools
    except ImportError:
        print("警告: 未安装mss库，将使用Pillow默认方式截图")
        print("如需精确控制多显示器，请安装: pip install mss")
        return take_screenshot(save_dir, monitor_index=None)
    
    # 创建保存目录（如果不存在）
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"screenshot_monitor{monitor_index}_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    
    try:
        with mss.mss() as sct:
            # 获取指定显示器
            monitor = sct.monitors[monitor_index]  # monitors[0]是虚拟屏幕，[1]是第一显示器
            
            # 截取该显示器
            screenshot = sct.grab(monitor)
            
            # 保存为PNG
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=filepath)
            
        return filepath
    except IndexError:
        print(f"错误: 显示器索引 {monitor_index} 超出范围")
        print(f"可用显示器数量: {len(sct.monitors) - 1}")
        return None
    except Exception as e:
        print(f"截图失败: {e}")
        return None


def scheduled_screenshot(interval=5, max_count=None, save_dir="screenshots", monitor_index=None):
    """
    定时截屏函数
    
    Args:
        interval: 截图间隔时间（秒），默认5秒
        max_count: 最大截图次数，None表示无限循环
        save_dir: 保存图片的目录
        monitor_index: 显示器索引，None=使用Pillow默认方式，1=第一显示器，2=第二显示器
    """
    print("=" * 60)
    print("定时截屏程序已启动")
    print(f"截图间隔: {interval} 秒")
    print(f"保存目录: {save_dir}")
    
    if monitor_index is None:
        print("截图模式: 主显示器（Pillow默认方式）")
    else:
        print(f"截图目标: 显示器 {monitor_index}（使用mss库）")
    
    if max_count:
        print(f"截图次数: {max_count} 次")
    else:
        print("截图模式: 持续运行 (按 Ctrl+C 停止)")
    print("=" * 60)
    print()
    
    count = 0
    try:
        while True:
            # 截取屏幕
            if monitor_index is not None:
                filepath = take_screenshot_with_pyscreenshot(save_dir, monitor_index)
            else:
                filepath = take_screenshot(save_dir, monitor_index=None)
            
            if filepath:
                count += 1
                
                # 显示进度信息
                if max_count:
                    print(f"[{count}/{max_count}] 截图已保存: {filepath}")
                else:
                    print(f"[{count}] 截图已保存: {filepath}")
                
                # 检查是否达到最大次数
                if max_count and count >= max_count:
                    print("\n已达到最大截图次数，程序退出。")
                    break
            else:
                print("截图失败，跳过本次")
            
            # 等待下一次截图
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断。")
        print(f"总共截取 {count} 张图片。")


if __name__ == "__main__":
    # ========== 配置区域 ==========
    INTERVAL = 10          # 截图间隔（秒）
    MAX_COUNT = None      # 最大截图次数，None表示无限循环，例如设置为10则只截取10次
    SAVE_DIR = "screenshots"  # 保存目录
    MONITOR_INDEX = 2     # 显示器索引：None=主显示器(Pillow)，1=第一显示器，2=第二显示器(扩展屏)
    # ==============================
    
    # 开始定时截屏
    scheduled_screenshot(
        interval=INTERVAL,
        max_count=MAX_COUNT,
        save_dir=SAVE_DIR,
        monitor_index=MONITOR_INDEX
    )
