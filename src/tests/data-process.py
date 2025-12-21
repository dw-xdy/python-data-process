import polars as pl

"""
关于编码问题:
    一般来说windows系统应该都是要转成 gbk 编码
    但是对于.xlsx来说, 一定是 UTF-8 编码(.xlsx只支持这一种格式),  
    对于读取.csv文件来说, polars必须要读取 UTF-8 编码
    所以一定要将 .csv 文件编码转成utf-8编码再进行读取.
    关于 .csv 文件的写入来说, polars 也是默认写入的是 UTF-8 编码.
    若是需要别的编码方式, 
    那么推荐使用 to_pandas 方法转成pandas类型再进行编码 (推荐使用utf-8-sig编码)
    polars没有原生的方式进行读取, 写入 .xlsx 文件
    所以需要两个额外的依赖: 
    读取: fastexcel   
    写入: xlsxwriter
    所以使用polars处理.xlsx文件不用关心编码问题.
"""

# 文件路径
csv_file = r"F:\备份\2_姐姐给我的词频统计代码用于学习\副本语料（1）.csv"

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
    .group_by("匹配项")  # 先根据"匹配项"这一列进行分组
    # .agg(pl.len().alias("出现次数")) # 然后通过 agg() 函数进行统计.
    .agg(
        pl.col("匹配项").count().alias("出现次数")
    )  # 这两种写法是完全一样的, 但是这里的区别我并不是非常明白.
    .sort("出现次数", descending=True)
)

# result = (
#     df.select(
#         pl.col("语料数据")
#         .str.extract_all(pattern)  # 提取所有匹配
#         .alias("匹配项")
#     )
#     .explode("匹配项")  # 展开列表
#     .filter(pl.col("匹配项").is_not_null())
#     .group_by("匹配项").len()  # 先根据"匹配项"这一列进行分组
#     .sort("len", descending=True)
# )

print(result)

# 写入excel文件
output_path = r"C:\Users\asus\Desktop\学校作业\kaishi\匹配结果.xlsx"

result.write_excel(output_path)

print(f"转换成功")


# 这里可以将其用.csv文件进行保存.并且可以指定编码
# 转换为pandas DataFrame，然后使用pandas的to_csv方法
# result_pd = result.to_pandas()
#
# # 指定编码保存（支持多种编码）
# result_pd.to_csv(
#     output_path,
#     index=False,  # 不保存索引
#     encoding="utf-8-sig",  # 既支持特殊符号，又能让 Excel 不乱码 (非常好!!!)
# )
