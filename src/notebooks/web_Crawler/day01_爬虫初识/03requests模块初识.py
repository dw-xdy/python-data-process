# 【一】requests模块介绍
# 【1】介绍
# ● Requests 是⽤Python语⾔编写，基于urllib，采⽤Apache2 Licensed开源协议的 HTTP 库。
# ● 它⽐ urllib 更加⽅便，可以节约我们⼤量的⼯作，完全满⾜HTTP测试需求。
# ● 是一个功能强大、简洁易用的第三方Python库，用于发送HTTP请求。

# 【2】来源
# ● 可以模拟发送http请求
# ● urlib2：内置库，不太好用，繁琐
# ● 封装出requests模块，应用非常广泛（公司，人）
#   ○ requests模块最初由Kenneth Reitz于2010年创建并开源，旨在提供一种更人性化的方式来发送HTTP请求。
#   ○ 它的出现填补了Python标准库中urllib和urllib2模块使用起来不够友好的问题。

# 【3】关于爬虫库作者的小插曲
# python requests 作者_知名 Python 库 Requests 作者 Kenneth Reitz 被指滥用捐款-CSDN博客
# ● Kenneth Reitz 是一位知名的Python爱好者和开源社区活跃分子。他也是许多其他流行Python工具的作者之一，比如tablib、pipenv等。
# ● Kenneth Reitz 众筹换电脑（性能跟不上了），捐钱（谷歌公司捐了），2 万 8 千美元
# ● 买了游戏设备，爆料出来，骗捐，辟谣

# 【二】http协议
# 【1】无状态
# 每个请求都是独立的，服务器不会保留客户端信息
# 【2】请求和响应模型
# 发起请求要符合 HTTP 的请求模型
"""
# 请求模型
请求首行 请求方式 请求路径 Http协议版本
请求头 K:V键值对
换行 \r\n
请求体 二进制数据
"""

"""
响应模型
响应首行 响应状态码 Http协议版本
响应头 K:V键值对
换行 \r\n
响应体 二进制数据
"""
# 【3】应用层协议
# 基于 TCP/IP 协议之上的应用层协议
# 【4】短连接
# 一次交互后就断开连接

# 【三】学会看浏览器的开发者模式
# （1）调试模式
# ● 通过右键浏览器页面并选择调试模式，可以打开开发者工具，方便进行调试和查看页面的相关信息。
# （2）Elements
# ● Elements面板用于查看和编辑网页的结构和内容，其中包括响应体中的HTML格式数据。
# （3）Console
# ● Console面板是开发者用于在JavaScript中输出调试信息的窗口，在这里可以查看通过console.log()等方法输出的内容。
# （4）Network
# ● Network面板用于监视和查看浏览器发送和接收的网络请求，包括AJAX请求。
# ● 可以查看所有请求或者仅显示XHR（XMLHttpRequest）请求。

# 【四】安装requests模块
# pip install requests
# 【五】初步使用
# 【1】导入requests模块
import requests

# 【2】确定目标网址 (向百度发送请求.)
target_url = "https://www.baidu.com/"

# 【3】使用 requests 模块模拟浏览器发起请求
# 在地址栏回车网址发起的是 GET 请求
response = requests.get(url=target_url)  # 除了 get 请求, 当然还有 post 请求.

# 【4】获取响应数据
# print(response)  # <Response [200]>
# 从服务器返回的 html 页面源码
# print(response.text) # 将返回的 源码数据转换成文本格式

# 发现返回的是乱码 ç¾åº¦ä¸ä¸ï¼ä½ å°±ç¥é

# 将响应对象的编码转换成我们可以识别的
response.encoding = "utf8"  # gbk / utf8 (一般来说, 只需要这两个就够了)
print(response.text)
