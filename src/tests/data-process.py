import polars as pl
import numpy as np
import re

# 文件路径
csv_file = r'F:\备份\2_姐姐给我的词频统计代码用于学习\副本语料（1）.csv'

# 使用polars对文件进行读取
df = pl.read_csv(csv_file)

# print(df)
#
# # 列出所有的列名字.
# print(df.columns)
#
# # 展示第一列, "语料数据"
# print(df.select('语料数据'))
#
# # 将语料数据转为对象数组
# print(df.select('语料数据').to_numpy())
#
# # 展示对应的数据类型.
# print(df.select('语料数据').to_numpy().dtype)

# 将语料数据的对象数组继续转为python中的list
# print(df.select('语料数据').to_numpy().tolist())

# 方法1：使用 Polars 直接统计（推荐）
result = (
    df.select(
        pl.col("语料数据")
        .str.extract_all(r"\[\[\[(.*?不堪.*?)\]\]\]")  # 提取所有匹配
        .alias("匹配项")
    )
    .explode("匹配项")  # 展开列表
    .filter(pl.col("匹配项").is_not_null())
    .group_by("匹配项")
    .agg(pl.len().alias("出现次数"))
    .sort("出现次数", descending=True)
)

print(result)

# # 方法2：如果一定要用字典（基于你提供的代码）
# sister_list = df.select('语料数据').to_numpy().tolist()
#
# sister_dict = {}
#
# for string in sister_list:
#     # 使用正则查找所有匹配
#     matches = re.findall(r'\[\[\[(.*?不堪.*?)]\]\]', str(string))
#     for match in matches:
#         sister_dict[match] = sister_dict.get(match, 0) + 1
#
# # 按次数排序
# sorted_dict = dict(sorted(sister_dict.items(), key=lambda x: x[1], reverse=True))
#
# print(sorted_dict)
#
# for (key, value) in sorted_dict.items():
#     print(f"{key} : {value}")