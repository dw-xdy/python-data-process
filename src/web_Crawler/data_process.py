import polars as pl
import json

# 读取JSON文件
df = pl.read_json(r"C:\Users\asus\Desktop\学校作业\通信原理\题目数据.json")

# 筛选answer不是'A','B','C','D','1','0'的记录（即剩下的题目）
filtered_df = df.filter(~pl.col("答案").is_in(["A", "B", "C", "D", "1", "0", ""]))

# 1. 保存为JSON文件（带缩进格式）
with open(r"C:\Users\asus\Desktop\学校作业\通信原理\剩下的题目.json", "w", encoding="utf-8") as f:
    json.dump(filtered_df.to_dicts(), f, ensure_ascii=False, indent=2)

# 2. 保存为Excel文件
filtered_df.write_excel(r"C:\Users\asus\Desktop\学校作业\通信原理\剩下的题目.xlsx")

print(f"原始数据共 {df.height} 条记录")
print(f"选择题+判断题共 {df.height - filtered_df.height} 条记录")
print(f"剩下的题目共 {filtered_df.height} 条记录")
print("已保存到：")
print(f"  - JSON文件：C:\\Users\\asus\\Desktop\\学校作业\\通信原理\\剩下的题目.json")
print(f"  - Excel文件：C:\\Users\\asus\\Desktop\\学校作业\\通信原理\\剩下的题目.xlsx")
