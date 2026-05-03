# 【一】响应数据格式
# 【1】以字符串的形式返回数据 response.text
# 一般用于 页面源码
"""
# 第一步：导入模块
import requests
from fake_useragent import UserAgent

# 第二步 指定目标地址
target_url = "https://www.sogou.com/web"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
headers = {
    'User-Agent': UserAgent().random
}

params = {
    "query": "小米15"
}

response = requests.get(url=target_url, headers=headers, params=params)
print(response.text)

"""

# 【2】以二进制的形式返回数据 response.content
# 一般用于 图片/视频/压缩包/pdf文档/word文档
"""
# 第一步：导入模块
import requests
from fake_useragent import UserAgent

# 第二步 指定目标地址
target_url = "https://pic.netbian.com/uploads/allimg/241030/083910-1730248750fbc5.jpg"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
headers = {
    'User-Agent': UserAgent().random
}

response = requests.get(url=target_url, headers=headers)
print(response.content)
"""
# 【3】以json格式的形式返回数据 response.json()
"""
import requests

# 定义目标地址
tag_url = "https://jsonplaceholder.typicode.com/users"

# 发送请求，获取响应数据
response = requests.get(tag_url)

# 将响应内容解析为 JSON 格式
data = response.json()

# 打印响应内容的数据类型
print(type(data))

# 打印解析后的 JSON 数据
print(data)

"""

# 【二】响应体编码格式 response.encoding
# 访问百度获取到的字符串形式的响应数据发现是乱码看不懂
# 于是我们对响应进行了编码
"""
import requests

# 定义目标地址
tag_url = "https://www.baidu.com"

# 发送请求，获取响应数据
response = requests.get(tag_url)

response.encoding = "utf8"  # utf-8 / gbk

# 将响应内容解析为 JSON 格式
data = response.text

# 打印解析后的 JSON 数据
print(data)

"""

# 【三】响应状态码 response.status_code
# 发起请求会返回响应状态码 我们可以根据响应状态码进行判断是否请求成功
"""
import requests

# 定义目标地址
tag_url = "https://www.baidu.com"

# 发送请求，获取响应数据
response = requests.get(tag_url)

print(response.status_code) # 302 重定向 / 403 禁止 / 200 请求成功
"""

# 【四】响应头 response.headers
"""
# 有的请求是多次中转的请求
# 
import requests

# 定义目标地址
tag_url = "https://www.baidu.com"

# 发送请求，获取响应数据
response = requests.get(tag_url)

print(response.headers)
"""

# 【五】响应Cookie response.cookies
# 有的请求 返回的响应 Cookie 会携带响应的信息
"""
import requests

# 定义目标地址
tag_url = "https://www.baidu.com"

# 发送请求，获取响应数据
response = requests.get(tag_url)

print(response.cookies.values())
print(response.cookies.keys())
print(response.cookies.items())
print(response.cookies.get_dict())
print(dict(response.cookies))
"""

# 【六】请求定向URL
# 有时候会发现地址在浏览器可以正常访问 但是代码就不行
# 一种是你的请求中的请求头参数带的不对
# 二是请求的地址被中转了 访问百度 ---> 中专到了 百度的安全验证页面

"""
import requests

# 定义目标地址
tag_url = "https://www.baidu.com/s?wd=%E5%91%A8%E6%9D%B0%E4%BC%A6"

# 发送请求，获取响应数据
response = requests.get(tag_url)

# 当前响应的 url response.url
'''
○ 这是在完成HTTP请求并接收到服务器响应后，实际返回的资源URL。
○ 在重定向发生时，这个属性会反映最终页面的实际URL。
○ 例如，如果你发起一个请求到某个网站A，但该网站随后重定向到了网站B，那么response.url将显示网站B的URL。
'''
print(response.url) # https://www.baidu.com/

# 当前响应的请求发起的地址 response.request.url
'''
○ 这是发送HTTP请求时使用的原始URL，即你在发出请求时指定的URL。
○ 无论是否发生重定向，这个属性始终保持不变。
○ 也就是说，它反映了你最初尝试访问的地址。
'''
print(response.request.url)
"""

# 【七】当前请求的重定向的URL
# 可以查看当前请求是否发生了重定向
"""
import requests

# 定义目标地址
tag_url = "https://www.baidu.com/s?wd=%E5%91%A8%E6%9D%B0%E4%BC%A6"

# 发送请求，获取响应数据
response = requests.get(tag_url)

print(response.history)  # [<Response [302]>]
print(response.history[0].request.url)  # https://www.baidu.com/s?wd=%E5%91%A8%E6%9D%B0%E4%BC%A6
print(response.request.url)
"""

# 【八】迭代获取二进制数据 response.iter_content(chunk_size=1024)
# 适用于大文件的二进制数据 一次性接受太大 分批次接受
"""
# 第一步：导入模块
import requests
from fake_useragent import UserAgent

# 第二步 指定目标地址
target_url = "https://pic.netbian.com/uploads/allimg/241030/083910-1730248750fbc5.jpg"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
headers = {
    'User-Agent': UserAgent().random
}

response = requests.get(url=target_url, headers=headers)
for chunks in response.iter_content(chunk_size=1024):
    print(chunks)
    print("-------")
"""
