import socket

def check_connectivity(address, port):
    try:
        with socket.create_connection((address, port), timeout=5) as s:
            return True  # 地址可连通
    except (socket.timeout, socket.error):
        return False  # 地址不可连通

# 示例
address = "http://60.205.191.88:23091/"
port = 80  # HTTP 默认端口
if check_connectivity(address, 23091):
    print(f"{address}:{port} 可连通")
else:
    print(f"{address}:{port} 不可连通")
