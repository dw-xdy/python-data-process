# 【一】导入模块
import requests
from fake_useragent import UserAgent

# 【二】确定目标网址
target_url = "http://www.aa7a.cn/user.php"

# 【三】带请求参数还是请求体
# 请求参数 parmas
# 请求体参数 data / json
# （1）json=data
# ● 当使用requests.post方法时
# ● 如果将data参数设置为一个字典，并同时将headers参数中的Content-Type设置为application/json
# 那么data字典将被自动序列化为JSON字符串，并作为请求的主体数据发送。
# ● 这样的请求方式常用于与服务器交互时，需要使用JSON格式进行数据传输的情况。
# （2）data=data
# ● 默认情况下，requests.post方法将会将data参数以application/x-www-form-urlencoded格式进行编码。
# ● 这种编码方式将字典数据转换成键值对的形式，并使用&符号进行连接。
# ● 然后，将生成的字符串作为请求的主体数据发送到服务器。这种方式常用于处理表单提交的场景。
# application/json
data = {
    "username": "",
    "password": "",
    "captcha": "P6Mu",
    "remember": "1",
    "ref": "http://www.aa7a.cn",
    "act": "act_login",
}

headers = {"User-Agent": UserAgent().random}

# 【四】发起请求获取响应对象
response = requests.post(url=target_url, headers=headers, json=data)

print(response.text)
# {"error":0,"ref":"http://www.aa7a.cn"}

print(response.cookies.items())
