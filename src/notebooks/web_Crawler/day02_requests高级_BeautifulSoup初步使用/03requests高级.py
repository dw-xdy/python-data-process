# 【一】代理
# 【1】引入
# 在摘取网络数据的时候你的请求都是从自己的电脑中的网线中发起的
# 一旦你的请求次数过多就会导致你的 IP 受限
# 这时候我们就需要借助带来完成请求中转
# 【2】代理的作用
# 通过代理可以帮助我们隐藏真是的IP地址，染过频次访问限制或者IP黑名单限制
# 【3】代理的匿名度
# （1）透明代理 --- 一般免费的都是透明
# 网站的服务器知道你使用了代理，也知道你的真实IP
# （2）匿名代理 --- 氪金
# 网站服务器知道你使用了代理，但是无法知道你的真实IP
# （3）高匿代理 --- 氪金 一般的服务器都是架设在 香港/澳门/菲律宾/ ...
# 网站服务器不知道你使用了代理，也不知道你的真实IP

# 一般的黑客 大批量攻击别人的服务器  人家就会大批量的封
# 这时候的这些IP我们统称为肉鸡
# 如果到了公司实际生产中 高匿代理 ---> 去找老板要预算

# 【4】代理分为两种类型
# 根据你的请求协议分
# HTTP   ： 本地的这或者你的服务器的IP
# HTTPS  ： 需要额外的证书进行校验 SSL 证书校验

# 现在常见的网站的请求协议都是  HTTPS 协议

# 【5】代理如何添加
# （1）requests 对象携带代理
'''
# 第一步 导入requests模块
import requests
from fake_useragent import UserAgent

# 第二步 定义目标地址
tag_url = "https://www.baidu.com"

# 第三步 发送请求，获取响应数据
# （1）做一个请求头的伪装
headers = {
    "User-Agent": UserAgent().random
}
# （2）携带代理
proxies = {
    "http": "http://127.0.0.1:8000/",
    "https": "https://127.0.0.1:8000/",
}
response = requests.get(tag_url, headers=headers,proxies=proxies)
'''
# （2）session 对象携带代理
"""
# 第一步 导入requests模块
import requests
from fake_useragent import UserAgent

session = requests.Session()


# 第二步 定义目标地址
tag_url = "https://www.baidu.com"

# 第三步 发送请求，获取响应数据
# （1）做一个请求头的伪装
headers = {
    "User-Agent": UserAgent().random
}
# （2）携带代理
proxies = {
    "http": "http://127.0.0.1:8000/",
    "https": "https://127.0.0.1:8000/",
}

# 方式一
'''
# 主动给session对象设置代理
session.proxies = proxies
# 发起请求就不需要额外再携带代理
response = session.get(tag_url, headers=headers)
'''

# 方式二：跟requests对象一样携带在请求中
response = session.get(tag_url, headers=headers, proxies=proxies)
"""

# 【6】付费代理
# 网上搜 一定有 只需要氪金 就能用

# 【7】免费代理
# 自己找网上多的是 但是一般都是无效的

# 【二】SSL认证
# https = http + ssl 证书
# 在某些网站会让我们校验 ssl 证书但是某些情况下我们是不想校验的
# 这时候就需要指定一个参数 取消 ssl 认证

# 【1】不携带证书就会报错
'''
import requests
url = 'https://ssr2.scrape.center/'
response = requests.get(url)
print(response.status_code)
# requests.exceptions.ConnectionError: 
# HTTPSConnectionPool(host='ssr2.scrape.center', port=443): 
# Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x13a9d52d0>: Failed to establish a new connection: 
# [Errno 8] nodename nor servname provided, or not known'))
'''
# 【2】取消证书验证
'''
import requests
url = 'https://ssr2.scrape.center/'
response = requests.get(url=url, verify=False)
print(response.status_code)
# InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
#   warnings.warn((
# 200
'''

# 【3】加上证书验证
'''
import requests
url = 'https://ssr2.scrape.center/'
cert_file = "/path/to/my_certificate.pem"

# 发送请求，并使用自定义证书进行 SSL 验证
response = requests.get(url, verify=cert_file)

# 打印响应状态码
print(response.status_code)

# 打印响应内容
print(response.text)
'''

# 【三】超时时间设置
# 在某些情况下我们会访问指定网站超时 给她加一个超时时间

# 超出指定时间未响应后会直接抛出异常终止访问

# ● 网络请求不可避免会遇上请求超时的情况，在 requests 中，如果不设置你的程序可能会永远失去响应。
# ● 超时又可分为连接超时和读取超时。
# ● 在使用requests模块时，可以通过设置超时参数来控制请求的超时时间。
# ● 超时参数可以是一个浮点数或一个元组。
# ● 如果超时参数是一个浮点数，它表示接收数据的超时时间，单位为秒。
#   ○ 例如，timeout=0.1代表接收数据的超时时间为0.1秒。
# ● 如果超时参数是一个元组，它包含两个值，分别表示连接超时时间和接收数据的超时时间，单位同样为秒。
#   ○ 例如，timeout=(0.1, 0.2)代表连接超时时间为0.1秒，接收数据的超时时间为0.2秒。


# 【1】连接超时
'''
import time
import requests

# 定义目标地址
url = 'http://www.google.com.hk'

# 打印开始时间
print(time.strftime('%Y-%m-%d %H:%M:%S'))

# 异常捕获
try:
    # 尝试获取目标地址响应
    response = requests.get(url, timeout=(5,10)).text
    print('success')
# 如果遇到超时异常，则捕获并打印异常信息
except requests.exceptions.RequestException as e:
    print(e)

# 打印结束时间
print(time.strftime('%Y-%m-%d %H:%M:%S'))
'''
# 【2】超时重试
'''
# （1）方案一：自己写 while 循环
# （2）方案二：借助 requests 对象中的重试对象
import time
import requests
from requests.adapters import HTTPAdapter

session = requests.Session()
# 设置 HTTP 请求最大重试次数为3
session.mount('http://', HTTPAdapter(max_retries=3))
# 设置 HTTPS 请求最大重试次数为3
session.mount('https://', HTTPAdapter(max_retries=3))

# 记录开始时间
print(time.strftime('%Y-%m-%d %H:%M:%S'))
try:
    # 发送 GET 请求，获取响应对象
    response = session.get('http://www.google.com.hk', timeout=2)
    page_text = response.text
    print(page_text)
except requests.exceptions.RequestException as e:
    print(e)
print(time.strftime('%Y-%m-%d %H:%M:%S'))
'''

# 【四】高级身份认证
'''
# 在某些网站我们需要进行身份的认证
# 需要先登陆 登录后获取到认证信息才能继续使用网站
from requests.auth import HTTPBasicAuth
import requests

# 创建一个使用 'user' 和 'pass' 进行基本身份验证的函数。
# user 用户名 pass 密码
basic = HTTPBasicAuth('user', 'pass')

# 然后使用该函数进行请求。
response = requests.get('https://httpbin.org/basic-auth/user/pass', auth=basic)

# 输出响应的文本。
print(response.text)
# {
#   "authenticated": true, 
#   "user": "user"
# }

# 输出响应的状态码。
print(response.status_code)
# <Response [200]>
'''

# 【2】简写语法
'''
import requests

# 携带认证参数，使用该函数进行请求。
response = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))

# 输出响应的文本。
print(response.text)
# {
#   "authenticated": true, 
#   "user": "user"
# }

# 输出响应的状态码。
print(response.status_code)
# <Response [200]>
'''

# 【五】异常捕获
# 在 requests 对象中内置了很多的异常信息
# from requests.exceptions import ConnectionError, SSLError, RetryError, ReadTimeout
# 捕获制定异常的前提是 自己 知道会发生那些异常 再去进行定制化解决方案
# 为了你的程序的健壮性


# 【六】文件上传
'''
import requests

files = {'file': open('a.jpg', 'rb')}
response = requests.post('http://httpbin.org/post', files=files)
print(response.status_code)


# 我们在Django写 BBS 注册时候也带过头像文件
'''