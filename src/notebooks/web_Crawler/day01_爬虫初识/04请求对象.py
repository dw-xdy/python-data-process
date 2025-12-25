# GET 请求
# 【一】请求方式
# 【1】HTTP默认的请求方式
# GET 请求
# 浏览器地址栏回车默认是
# form表单默认的请求方式
# Ajax的默认请求方式

# 【2】GET请求的特点
# 所有的请求参数都会携带在路径中
# 因为携带在路径中 所以请求提数据就不能太大 1MB 之内

# 【3】发送get‘请求
"""
# 【1】导入requests模块
import requests

# 【2】确定目标网址
# target_url = 'https://www.baidu.com/'

# 【3】使用 requests 模块模拟浏览器发起请求
# 在地址栏回车网址发起的是 GET 请求
response = requests.get(url=target_url)
"""

# 【二】请求体参数
# 【1】导入模块
import requests

# 【2】确定目标地址
# target_url = "https://www.baidu.com/s?wd=%E5%91%A8%E6%9D%B0%E4%BC%A6"
#
# # 【3】发起请求、
# response = requests.get(url=target_url)
# response.encoding = "utf8"
# # print(response.text)      # 百度安全验证 网络不给力，请稍后重试 返回首页 (风险控制)
# # 【4】请求参数之查看请求头参数 response.request.headers (这是响应对象的请求头)
# print(response.request.headers)
"""
这是我的 User-Agent
{'User-Agent': 'python-requests/2.32.5', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive'}

实际浏览器的: User-Agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
"""


# 【5】修改请求头参数
"""
params = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
# 让请求携带参数
response = requests.get(url=target_url, params=params)
response.encoding = "utf8"
print(response.request.url)
print(response.text)
"""



# ● 常见的HTTP头部字段包括：
#   ○ Host：指定目标服务器的域名或IP地址。
#   ○ User-Agent：标识发送请求的用户代理（通常是浏览器）。
#     ■ PC浏览器
#     ■ APP浏览器
#     ■ Linux
#     ■ macOS
#   ○ Accept：指定客户端能够接收的内容类型。
#   ○ Content-Type：指定请求或响应中实体的媒体类型。
#   ○ Content-Length：指定实体主体的长度（以字节为单位）。
#   ○ Cookie：向服务器传递保存在客户端的cookie信息。
#   ○ Cache-Control：指定如何缓存和重新验证响应。
#   ○ Referer：大型网站通常都会根据该参数判断请求的来源

# 【6】请求头之 User-Agent 模块
"""
# pip install fake-useragent
from fake_useragent import UserAgent
# print(UserAgent().random)  # 只要执行一次, 那么就会随机给你一个内核.
headers = {
    'User-Agent':UserAgent().random   # 这里一般直接进行替换.
}
# 让请求携带参数
response = requests.get(url=target_url, headers=headers)
response.encoding = "utf8"
# print(response.request.url)
print(response.text)
"""

# 【三】请求参数编码

# 【1】方式一 利用urlencode编码
"""
from urllib.parse import urlencode
from fake_useragent import UserAgent

keyword = {
    "wd": "周杰伦"
}
'''
print(urlencode(keyword, encoding="utf8"))  # 传入一个字典, 使用utf-8编码进行解析
# wd=%E5%91%A8%E6%9D%B0%E4%BC%A6
# wd=%E5%91%A8%E6%9D%B0%E4%BC%A6
'''
target_url = 'https://www.baidu.com/s?' + urlencode(keyword, encoding="utf8")

headers = {
    "User-Agent": UserAgent().random
}

print(target_url)
# https://www.baidu.com/s?wd=%E5%91%A8%E6%9D%B0%E4%BC%A6
# https://www.baidu.com/s?wd=%E5%91%A8%E6%9D%B0%E4%BC%A6

response = requests.get(url=target_url, headers=headers)
response.encoding = "utf8"
print(response.request.url)
print(response.text)
"""

# 【2】方案二：requests模块内置了 url 编码
from fake_useragent import UserAgent

# 这里需要注意的是: 这里的请求是发送到搜狗的, 所以对应的, 需要修改请求参数 将 wd 修改为: query
# headers的作用和意义: 用来标识你是一个正常的浏览器发送的请求, 而不是一个python程序发送的请求
headers = {
    "User-Agent": UserAgent().random
}

params = {
    "query": "周杰伦"
}

target_url = 'https://www.sogou.com/web?'

response = requests.get(url=target_url, headers=headers, params=params)

print(response.text)
# with open("01.html", "w", encoding="utf8") as fp:
#     fp.write(response.text)
