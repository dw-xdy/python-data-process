# 【一】爬虫
# 爬虫就是通过代码自动化获取网页上的可视化数据的程序
# 【2】分类
# 通用爬虫和定向爬虫
# 基于规则的爬虫和基于机器学习的爬虫
# 单机爬虫和分布式爬虫
# 【3】常用的第三方库
# requests : 用来发送http请求的
# BeautifulSoup
# lxml
# Scrapy
# Selenium
# ...
# 【4】注意事项
# 合法
# 注意速度
# 稳定性
# 数据存储的合理性

# 【5】常见的反扒措施
# 频率限制 1min 3次
# 封IP 或者 账号
# 请求头中方加密信息
# 响应数据加密
# 验证码
# JS加密
# ...

# 【二】requests模块
# 【1】安装
# pip install requests
# 【2】模拟浏览器的请求的步骤
'''
# 第一步：导入模块
import requests

# 第二步 指定目标地址
target_url = "https://www.baidu.com"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
response = requests.get(url=target_url)

# 第四步 提取响应对象中返回的数据 (以字符串形式返回的响应数据)
page_text = response.text
'''

# 【3】请求相关的参数
# （1）浏览器默认的请求是GET请求
# 你要发送 get 请求就直接 requests.get
# 你要发送 post 请求就直接 requests.post

# （2）在只指定目标地址访问百度的时候会发现访问不到
# 去看了浏览器的包 发现期终有一个参数是 User-Agent (浏览器的标识信息)
'''
# 第一步：导入模块
import requests

# 第二步 指定目标地址
target_url = "https://www.sogou.com/web?query=%E5%B0%8F%E7%B1%B3SU7+Ultra%E9%A2%84%E5%94%AE%E4%BB%B781.49%E4%B8%87%E5%85%83"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
response = requests.get(url=target_url)

print(response.request.headers)
zz# {'User-Agent': 'python-requests/2.20.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Cookie': 'ABTEST=0|1730249820|v17; SNUID=2D8B28BFCBCCEE6DE63BCD23CB971ADE; IPLOC=CN3100; SUID=E741E2746B54A20B000000006721845C; cuid=AAGD+oqRTwAAAAuiUb+1/AAAEAM='}

# 第四步 提取响应对象中返回的数据 (以字符串形式返回的响应数据)
page_text = response.text
# 此验证码用于确认这些请求是您的正常行为而不是自动程序发出的，需要您协助验证。

with open("01.html","w",encoding="utf-8") as fp:
    fp.write(page_text)
'''
# （3）携带请求头参数
# 请求头是一定要携带的, 因为这毕竟是需要用浏览器来发出请求, 如果 User-Agent 是 python 的话会失败
'''
# 第一步：导入模块
import requests

# 第二步 指定目标地址
target_url = "https://www.sogou.com/web?query=%E5%B0%8F%E7%B1%B3SU7+Ultra%E9%A2%84%E5%94%AE%E4%BB%B781.49%E4%B8%87%E5%85%83"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
# :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}
response = requests.get(url=target_url,headers=headers)

print(response.request.headers)
# {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}

# 第四步 提取响应对象中返回的数据 (以字符串形式返回的响应数据)
page_text = response.text
# 此验证码用于确认这些请求是您的正常行为而不是自动程序发出的，需要您协助验证。

with open("02.html", "w", encoding="utf-8") as fp:
    fp.write(page_text)
'''
# （3）模块之随机请求头中的User-Agent
'''
# pip install fake-useragent
from fake_useragent import UserAgent

print(UserAgent().random)
'''

# （4）请求参数携带
# [1] 自己使用 urlencode 编码
'''
from urllib.parse import urlencode
# 字典形式的数据
# 小米SU7 Ultra预售价81.49万元
keyword = {
    "query":"小米SU7 Ultra预售价81.49万元"
}
print(urlencode(keyword,encoding="utf8"))
# query=%E5%B0%8F%E7%B1%B3SU7+Ultra%E9%A2%84%E5%94%AE%E4%BB%B781.49%E4%B8%87%E5%85%83
# query=%E5%B0%8F%E7%B1%B3SU7+Ultra%E9%A2%84%E5%94%AE%E4%BB%B781.49%E4%B8%87%E5%85%83
'''
# [2] requests模块内置的 url 编码
'''
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

# 第四步 提取响应对象中返回的数据 (以字符串形式返回的响应数据)
page_text = response.text
# 此验证码用于确认这些请求是您的正常行为而不是自动程序发出的，需要您协助验证。

with open("03.html", "w", encoding="utf-8") as fp:
    fp.write(page_text)

'''

# （5）响应中的Cookie信息
# 以雪球网为例 ： 必须访问官网后获取到 Cookie 信息才能继续访问他的后续数据
# 没有访问雪球网直接访问数据发现访问根本行不通

# [1] 先访问雪球网 获取到 Cookie信息
# 第二步 把 Cookie 信息添加到 下一次的请求头中
'''
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

cookie_dict = dict(response.cookies)

params = {
    "query": "小米16"
}
# 方式一：直接携带Cookie字典
response = requests.get(url=target_url, headers=headers, params=params, cookies=cookie_dict)
# 方式二：将字典转为字符串携带在请求头中
headers = {
    'User-Agent': UserAgent().random,
    "Cookies":f"SUID=6DCB15242D53960A000000006581056C; cuid=AAF9IJs2SQAAAAqMWj27mAEAHgc=; SUV=1702954348852738; ssuid=868722000; ABTEST=0|1730249517|v17; IPLOC=CN3100; SNUID=C462C15723220183058514A4247C0705; LSTMV=99%2C120; LCLKINT=138979"
}

'''

# [2] requests 对象中有一个 对象 校 session 对象
# session 就是保存信息的 直接用 session 代替 requests 发起请求
# 发起请求后产生的 Cookie 信息回自动携带 在 session 对象中
'''
# 第一步：导入模块
import requests
from fake_useragent import UserAgent

# 生成 session 对象
session = requests.Session()

# 第二步 指定目标地址
target_url = "https://www.sogou.com/web"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
headers = {
    'User-Agent': UserAgent().random
}

params = {
    "query": "小米15"
}

response = session.get(url=target_url, headers=headers, params=params)
params = {
    "query": "小米16"
}

response = session.get(url=target_url, headers=headers, params=params)

'''
# 【三】requests请求之POST请求
# get请求的请求体参数是携带在请求路径中的
# post 请求的请求体数据是携带 在二进制数据中的

# 花花手机 的登陆操作
# 第一步：导入模块
import requests
from fake_useragent import UserAgent

# 生成 session 对象
session = requests.Session()

# 第二步 指定目标地址
target_url = "http://www.aa7a.cn/user.php"

# 第三步 模拟浏览器发起GET请求 , 获取响应对象
headers = {
    'User-Agent': UserAgent().random
}

params = {
    "ref": "http://www.aa7a.cn"
}

# 第四步 定义请求体参数
data = {
    'username': 'z2068946849@163.com',
    'password': 'sda',
    'captcha': '萨达',
    'remember': '1',
    'ref': 'http://www.aa7a.cn',
    'act': 'act_login',
}

# data = data
# json = data : accept: application/json, text/javascript, */*
response = session.post(url=target_url, headers=headers, json=data,params=params)

# data = data  登陆成功后会返回一个字典
# json = data 登陆成功后会返回一个登陆成功后的页面

print(response.request.url)
# http://www.aa7a.cn/user.php?ref=http%3A%2F%2Fwww.aa7a.cn
