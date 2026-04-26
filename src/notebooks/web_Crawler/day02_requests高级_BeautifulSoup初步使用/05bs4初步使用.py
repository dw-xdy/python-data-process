# 【soup对象中的四个对象】
from bs4 import BeautifulSoup

html_doc = open("html_doc.html", "r").read()

# 【一】BeautifulSoup 对象
# 指最外层的HTML文档对象
# soup 就是指 BeautifulSoup 对象
# soup = BeautifulSoup(html_doc, "lxml")


# 【二】Tag对象
# tag就是标签的意思
# tag对象就是指标签对象 我么可以获取到指定的标签对象
soup = BeautifulSoup(html_doc, "lxml")

# 【1】查找指定的标签对象
# （1）查找 head 标签的类型
# print(soup.head,type(soup.head)) # <class 'bs4.element.Tag'>
'''
<head>
<title>The Dormouse's story</title>
</head>
'''

# （2）获取到 title 标签
# print(soup.title)
'''
<title>The Dormouse's story</title>
'''
# （3）获取到所有的a标签
# print(soup.a)
'''
<a class="sister" href="http://example.com/outside" id="link_outside">p标签外面的a标签</a>
'''
# print(soup.p.a) # 第一个 p 标签下面的 a 标签 但是 第一个 p 标签下面没有 a 标签
# print(soup.p.b) # 第一个 p 标签下面的 p 标签 有就被拿出来了
'''
<b>The Dormouse's story</b>
'''

# 【2】获取指定标签对象的属性
"""
print(soup.a)
'''
<a class="sister" href="http://example.com/outside" id="link_outside">p标签外面的a标签</a>
'''

# （1）获取到当前标签的名字
print(soup.a.name)  # a
# （2）获取到当前a标签的属性值
print(soup.a["href"])  # http://example.com/outside
print(soup.a["class"])  # ['sister']
# （3）一次性获取标签的所有属性名和属性值
print(soup.a.attrs)  # {'href': 'http://example.com/outside', 'class': ['sister'], 'id': 'link_outside'}
"""
# 【3】修改指定标签的属性值
'''
print(soup.a.attrs)
# （1）将 href 属性替换掉 sister 和 brother
soup.a["class"] = "sister brother"
print(soup.a)
'''
# 【4】想要a标签中间的文本内容

'''
# （1）soup.a.string 针对与单个标签来说的
print(soup.p.string)  # p标签外面的a标签
# None

print(soup.p.strings)
# <generator object Tag._all_strings at 0x11e6c9c40>
for i in soup.a.strings:
    print(i)  # p标签外面的a标签
    # Elsie
'''

# 【三】NavigableString对象
print(type(soup.p.b.strings))
# <class 'generator'>
'''
# 表示标签中间的文本内容
# 获取p标签的文本内容
print(soup.p.string)  # 只能获取到当前 p 标签的文本信息
# None

# 获取p标签下所有的文本内容
print(soup.p.strings)
# <generator object Tag._all_strings at 0x102b7b300>

for i in soup.p.strings:
    print(i)
    print("-----")
# The Dormouse's story
'''

# 【四】Comment对象
# 主要用于获取标签中间的注释内容的对象
print(soup.b.string,type(soup.b.string))
# <class 'bs4.element.Comment'>