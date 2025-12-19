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

reg = r"\[\[\[(.*?不堪.*?)\]\]\]"

pattern = r"\[\[\[([\u4E00-\u9FA5]{2}不堪)\]\]\]"

# 方法1：使用 Polars 直接统计（推荐）
result = (
    df.select(
        pl.col("语料数据")
        .str.extract_all(pattern)  # 提取所有匹配
        .alias("匹配项")
    )
    .explode("匹配项")  # 展开列表
    .filter(pl.col("匹配项").is_not_null())
    .group_by("匹配项")
    .agg(pl.len().alias("出现次数"))
    .sort("出现次数", descending=True)
)

print(result)

# 写入CSV文件
output_path = r"C:\Users\asus\Desktop\学校作业\kaishi\匹配结果1.csv"

# 转换为pandas DataFrame，然后使用pandas的to_csv方法
result_pd = result.to_pandas()

# 指定编码保存（支持多种编码）
result_pd.to_csv(
    output_path,
    index=False,  # 不保存索引
    encoding='gbk',  # Windows中文系统常用
    # encoding='utf-8-sig',  # 带BOM的UTF-8，Excel兼容性好
    # encoding='utf-8',      # 标准UTF-8
)

