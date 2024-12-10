import requests

def test_http_connectivity(url):
    try:
        response = requests.get(url, timeout=5)  # 设置 5 秒超时
        if response.status_code == 200:
            print(f"{url} 可连通，返回状态码: {response.status_code}")
            return True
        else:
            print(f"{url} 返回状态码: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"{url} 不可连通，错误: {e}")
        return False

# 测试地址
url = "http://60.205.11.88:23091/"
test_http_connectivity(url)
