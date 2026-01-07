import socket

def test_telnet(host, port, timeout=10):
    """
    测试Telnet连接是否成功
    :param host: 目标IP地址
    :param port: 目标端口
    :param timeout: 超时时间（秒）
    :return: 连接结果字符串
    """
    try:
        # 创建socket对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # 尝试建立连接
        sock.connect((host, port))
        sock.close()
        return f"✅ 成功连接到 {host}:{port}"
    except socket.timeout:
        return f"⛔ 连接超时（{timeout}秒）"
    except ConnectionRefusedError:
        return f"❌ 连接被拒绝（端口未开放或防火墙拦截）"
    except socket.gaierror:
        return f"❌ 主机名解析失败（请检查IP地址）"
    except Exception as e:
        return f"⚠️ 未知错误: {str(e)}"

if __name__ == "__main__":
    # 配置目标地址和端口
    TARGET_IP = "http://112.1.78.178"
    TARGET_PORT = 1935
    
    # 执行测试并打印结果
    result = test_telnet(TARGET_IP, TARGET_PORT)
    print(f"测试目标: {TARGET_IP}:{TARGET_PORT}")
    print(result)