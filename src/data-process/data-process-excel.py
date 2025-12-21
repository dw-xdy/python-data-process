import polars as pl

"""
关于编码问题:
    对于.xlsx来说, 一定是 UTF-8 编码(.xlsx只支持这一种格式),  
    polars也只能读取和写入 UTF-8 编码
    polars没有原生的方式进行读取, 写入 .xlsx 文件
    所以需要两个额外的依赖: 
    读取: fastexcel   
    写入: xlsxwriter
    所以使用polars处理.xlsx文件不用关心编码问题.
    当然也可以选择使用.xlsx读取, 用.csv输出, 或者反过来, 这完全是看自己的想法了.
"""

# 文件路径
xlsx_file = r"F:\备份\2_姐姐给我的词频统计代码用于学习\副本语料（1）.xlsx"

# 使用polars对文件进行读取
df = pl.read_excel(xlsx_file)

pattern = r"\[\[\[([\u4E00-\u9FA5]{2}不堪)\]\]\]"

result = (
    df.select(
        pl.col("语料数据")
        .str.extract_all(pattern)  # 提取所有匹配
        .alias("匹配项")
    )
    .explode("匹配项")  # 展开列表
    .filter(pl.col("匹配项").is_not_null())
    .group_by("匹配项")
    .len()  # 先根据"匹配项"这一列进行分组
    .sort("len", descending=True)
)

print(result)

# 写入excel文件
output_path = r"C:\Users\asus\Desktop\学校作业\kaishi\匹配结果.xlsx"

result.write_excel(output_path)

print(f"转换成功")
