import polars as pl
import re


# 文件路径
csv_file = r"F:\备份\2_姐姐给我的词频统计代码用于学习\副本语料（1）.csv"

# 使用polars对文件进行读取
df = pl.read_csv(csv_file)

pattern = r"\[\[\[([\u4E00-\u9FA5]{2}不堪)\]\]\]"

res = df.get_column("语料数据").to_list()

good_list = []

for ret in res:
    enough = ret.replace("[[[", "").replace("]]]", "")
    good_list.append(enough)


from pkuseg import pkuseg  # 导入类

ans_list = []

my_list = []

# 创建分词器
seg = pkuseg()

for ret in good_list:
    ans_list.append(seg.cut(ret))

for ans in ans_list:
    for true_ans in ans:
        if len(true_ans) == 4 and re.search(r'^[\u4E00-\u9FA5]{2}不堪$', true_ans):
            my_list.append(true_ans)


print(len(my_list))
enough = pl.DataFrame(my_list)
kaishi = enough.group_by("column_0").len().sort("len", descending=True)
print(kaishi)

output_path = r"C:\Users\asus\Desktop\学校作业\kaishi\匹配结果123.xlsx"

kaishi.write_excel(output_path)




