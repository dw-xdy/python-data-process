# 【一】介绍
# 【1】简言
# ● 简单来说，Beautiful Soup是python的一个库
# ● 最主要的功能是解析从网页抓取的数据。
# 【2】官方解释
# ● Beautiful Soup提供一些简单的、python式的函数用来处理导航、搜索、修改分析树等功能。
# ● 它是一个工具箱，通过解析文档为用户提供需要抓取的数据，因为简单，所以不需要多少代码就可以写出一个完整的应用程序。
# 【3】小结
# ● Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库
# ● 它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式
# ● Beautiful Soup会帮你节省数小时甚至数天的工作时间
# ● 你可能在寻找 Beautiful Soup3 的文档,Beautiful Soup 3 目前已经停止开发,官网推荐在现在的项目中使用Beautiful Soup 4。
# 官方文档: https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/

# 【二】安装
# pip install BeautifulSoup4

# 【三】基础使用之解析器
# 帮助我们生成文档对象的解析方式，有的解析器比较强大，好用
"""
:param features: Desirable features of the parser to be
 used. This may be the name of a specific parser ("lxml",
 "lxml-xml", "html.parser", or "html5lib") or it may be the
 type of markup to be used ("html", "html5", "xml"). It's
 recommended that you name a specific parser, so that
 Beautiful Soup gives you the same results across platforms
 and virtual environments.

"""
# from bs4 import BeautifulSoup
# soup = BeautifulSoup()
# 【1】内置解析器  "html.parser"
# 2.7版本开始就有了 自带的解析器 对中文容错率比较低 解析速度适中

# 【2】第三方  "lxml" / "lxml-xml" **** lxml
# pip install lxml
# "lxml" 相对于 PC 页面来说
# "lxml-xml" 对于 APP 上面的页面来说
# 解析比较快 容错率比较强

# 【3】"html5lib"
# 对hTML5比较友好 解析速度相对来说快一点

# 【四】初步的使用
# 【1】方法一
"""
# 第一步 先获取到html页面页面 requests 模块获取到了页面源码 保存到本地
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
page_text = response.text

with open("01.html", "w") as fp:
    fp.write(page_text)
'''
# 第二步 从本地中读取到当前的页面源码文档
# 第三步 交给 BeautifulSoup4 去解析
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("01.html", "r").read(), "lxml")
print(soup, type(soup))  # <class 'bs4.BeautifulSoup'>

"""
# 【2】方式二：直接写一段代码片段或者从网页上读取下来后直接给 BeautifulSoup
