import polars as pl
from datetime import datetime
from loguru import logger as log

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

start = datetime.now().timestamp()

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

end = datetime.now().timestamp()

log.info(f"{end - start}")

start = datetime.now().timestamp()

# 提取"匹配项"列为list
ans_list = result.get_column("匹配项").to_list()

my_list = []

me_list = []

for ans in ans_list:
    my_list.append(ans.replace("[[[", " "))

for my in my_list:
    me_list.append(my.replace("]]]", " "))


from pkuseg import pkuseg  # 导入类

# 创建分词器
seg = pkuseg()

count = 0

true_ans = []

for fenciqi in me_list:
    re_ans = seg.cut(fenciqi)
    if len(re_ans) == 1:
        print(f"文本: {fenciqi}")
        print(f"分词结果: {re_ans}")
        print(f"分词数量: {len(re_ans)}")
        print("-" * 30)
        true_ans.append(re_ans)
        count += 1

print(count)

end = datetime.now().timestamp()

log.info(f"{end - start}")

# 创建单列DataFrame，列名为"词语"
enough = pl.DataFrame({"词语": true_ans})
print(enough)

