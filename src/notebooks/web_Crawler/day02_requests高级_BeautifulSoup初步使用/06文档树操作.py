# 【一】遍历文档树介绍
# 【1】什么是遍历文档树
# ● 遍历文档树，也被称为导航文档树，是指在一个文档对象模型（DOM）中按照特定的方法和规则来遍历和浏览其中的节点。
# ● DOM是一种处理XML或HTML文档的标准编程接口，它将文档解析成由节点和对象组成的树状结构。
# ● 在遍历文档树的过程中，可以通过访问当前节点及其相关属性、子节点、父节点、兄弟节点等信息，来对文档进行操作和分析。
# 【2】常见的文档树遍历算法
# ● 选择起始节点：
#   ○ 首先需要确定遍历的起始节点，可以是整个文档的根节点，也可以是某个指定的节点。
# ● 访问当前节点：
#   ○ 从起始节点开始，首先访问当前节点，可以获取当前节点的标签名、属性、文本内容等信息。
# ● 处理当前节点：
#   ○ 根据需要，对当前节点进行一些处理操作，比如判断节点类型、执行特定的任务等。
# ● 遍历子节点：
#   ○ 如果当前节点有子节点，将从第一个子节点开始递归遍历，重复步骤2和步骤3。
# ● 遍历兄弟节点：
#   ○ 如果当前节点没有子节点或者子节点已经遍历完毕，将继续遍历当前节点的下一个兄弟节点，重复步骤2和步骤3。
# ● 返回父节点：
#   ○ 当遍历到某个节点的兄弟节点都被遍历完毕后，返回到该节点的父节点，并继续遍历父节点的下一个兄弟节点。
# ● 结束条件：
#   ○ 当整个文档树的节点都被遍历完毕，或者满足某个结束条件时，结束遍历过程。
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("html_doc.html", "r").read(), "lxml")
# 【二】基础操作
"""
# 【1】获取当前标签的名字
print(soup.a.name)
# 【2】获取标签的属性值
print(soup.a["href"])
# 【3】获取标签中间的文本内容
# （1）获取到单个标签内容的单个内容
print(soup.a.string)  # Elsie
# （2）获取当前标签下的所有标签内容
print([i for i in soup.p.strings])  # ['\n', "The Dormouse's story", '\n']
# （3）获取当前标签下的文本内容
print(soup.a.text)  # Elsie
# （4）获取当前标签下的所有标签内容 但是去除掉 空格或换行
print([i for i in soup.p.stripped_strings])  # ["The Dormouse's story"]
"""
# 【三】嵌套选择
"""
# 可以在同一个对象上 . 后续取值
print(soup.head.title.text) # The Dormouse's story
print(soup.p.b.text) # The Dormouse's story
"""

# 【四】后代选择
# 可以通过 .contents 和.children 属性来获取标签的子节点。
# 【1】.contents 获取当前标签下的所有子节点和文本内容
# print(soup.p.contents)
"""
['\n    Once upon a time there were three little sisters; and their names were\n\n    ', <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, ',\n    ', <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, ' and\n    ', <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>, ';\n    and they lived at the bottom of a well.\n']
"""
# 【2】.children  迭代器对象
# print(soup.p.children)  # <list_iterator object at 0x12a509840>
# print([i for i in soup.p.children])
"""
['\n    Once upon a time there were three little sisters; and their names were\n\n    ', <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, ',\n    ', <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, ' and\n    ', <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>, ';\n    and they lived at the bottom of a well.\n']
"""
# 【3】.descendants 获取到的事当期那标签下的所有内容和标签对象及标签对象中的文本内容
# print(soup.p.descendants) # <generator object Tag.descendants at 0x11ba11c40>
# print([i for i in soup.p.descendants])
"""
['\n    Once upon a time there were three little sisters; and their names were\n\n    ', <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, 'Elsie', ',\n    ', <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, 'Lacie', ' and\n    ', <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>, 'Tillie', ';\n    and they lived at the bottom of a well.\n']
"""
# 【4】.parent 和 .parents
# （1）.parent 获取当前标签的父标签对象
# print(soup.a.parent)
"""
<p class="story">
    Once upon a time there were three little sisters; and their names were

    <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
    <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
    and they lived at the bottom of a well.
</p>
"""
# （2）.parents 获取到当前标签对象的所有父标签对象
"""
print(soup.a.parents) # <generator object PageElement.parents at 0x11cc69c40>
print([i for i in soup.a.parents])
"""

# 【5】.next_sibling 获取到当前标签的下一个兄弟对象
print(soup.a.next_sibling)  # ,
print(soup.a.next_sibling.next_sibling)
"""
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
"""

print(soup.a.previous_sibling.previous_sibling)  # 上一个兄弟

print(list(soup.a.next_siblings))  # 下面的兄弟们=>生成器对象

print(list(soup.a.previous_siblings))  # 上面的兄弟们=>生成器对象
